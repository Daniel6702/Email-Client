import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64
import msal
import json
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import email_util
from urllib.parse import urlparse, parse_qs
from html import escape

class GmailService():
    def __init__(self):
        self.flow = Flow.from_client_secrets_file(
            'Certificates\client_secret_google.json', 
            scopes=['https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/gmail.modify'], 
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        self.service = None

    def login(self):
        authorization_url, state = self.flow.authorization_url(access_type='offline', prompt='consent')
        webbrowser.open(authorization_url)

    def set_service(self, args):
        self.flow.fetch_token(authorization_response=args)
        credentials = self.flow.credentials
        self.service = build('gmail', 'v1', credentials=credentials)
    
    def send_email(self, email):
        message = self.create_message(email)
        user_id = email.from_email
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print("Message sent: %s" % message['id'])
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def is_html(self, text):
        tags = ['<html>', '<head>', '<body>', '<p>', '<br>', '<h1>', '<h2>', '<div>']
        return any(tag in text.lower() for tag in tags)

    def create_message(self, email):
        message = MIMEMultipart()
        message['to'] = ', '.join(email.to_email) 
        message['subject'] = email.subject

        if self.is_html(email.body):
            # Body contains HTML tags, assume it's HTML
            part = MIMEText(email.body, 'html')
        else:
            # Assume body is plain text
            part = MIMEText(email.body, 'plain')

        message.attach(part)

        for attachment in email.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment['file_data'])
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment["file_name"]}"')
            message.attach(part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}
    
    def get_emails(self, number_of_mails = 10, includeSpamTrash = False):
        #Query Search operators you can use with Gmail: https://support.google.com/mail/answer/7190?hl=en 
        #gets a list of email id's from api. for each id get message data. extracte relevant information and attachments. create list email objects. return list
        messages = self.list_messages('me', query='in:inbox', number_of_emails=number_of_mails, includeSpamTrash = includeSpamTrash)
        email_list = []

        for message in messages:
            message_data = self.get_message('me', message['id'])
            from_email, to_email, subject, body, attachments = self.extract_data_from_message(message_data)
            email = email_util.Email(from_email, to_email, subject, body, attachments)
            email_list.append(email)

        return email_list
    
    def list_messages(self, user_id, query='', number_of_emails = 10, includeSpamTrash = False):
        try:
            response = self.service.users().messages().list(userId=user_id, q=query, maxResults = number_of_emails, includeSpamTrash = includeSpamTrash).execute() #number_of_emails MAX = 500. includeSpamTrash: Include messages from SPAM and TRASH in the results
            messages = response.get('messages', [])
            return messages
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_message(self, user_id, message_id):
        try:
            message = self.service.users().messages().get(userId=user_id, id=message_id).execute()
            return message
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def extract_data_from_message(self, message_data):
        headers = message_data['payload']['headers']
        from_email = next((header['value'] for header in headers if header['name'] == 'From'), None)
        to_email = next((header['value'] for header in headers if header['name'] == 'To'), None)
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)

        payload = message_data.get('payload', {})
        parts = payload.get('parts', [])

        html_content = self.extract_email_content(parts)
        attachments_list = self.extract_attachments(message_data['id'], parts)

        return from_email, to_email, subject, html_content, attachments_list
            
    def extract_email_content(self, parts): #Extract the html content of the email body
        html_content = ""
        text_content = ""
        
        for p in parts:
            mime_type = p.get("mimeType")
            body_data = p.get("body", {}).get("data")
            if not mime_type or not body_data:
                continue
            data = base64.urlsafe_b64decode(body_data).decode("utf-8")
            if mime_type == "text/html":
                html_content += data
            elif mime_type == "text/plain":
                text_content += data
                
        if not html_content and text_content:
            html_content = f"<html><body>{escape(text_content)}</body></html>"

        return html_content

    def extract_attachments(self, message_id, parts):
        attachments_list = []

        for part in parts:
            if part['filename']:  # There is an attachment
                mimeType = part.get('mimeType', '')

                # Check if this part is an actual file attachment
                if mimeType.startswith('application/') or mimeType in ['text/csv', 'text/plain']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = self.service.users().messages().attachments().get(userId='me', messageId=message_id, id=att_id).execute()
                        data = att['data']

                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    file_name = part['filename']

                    attachment_info = {
                        'file_data': file_data,
                        'file_name': file_name,
                        'attachment_id': att_id
                    }

                    attachments_list.append(attachment_info)

        return attachments_list
    


class OutlookService():
    def __init__(self):
        self.result = None

        with open('Certificates\client_secret_outlook.json', "r") as json_file:
            data = json.load(json_file)

        authority_url = "https://login.microsoftonline.com/common"
        self.app = msal.PublicClientApplication(
            data["client_id"],
            authority=authority_url,
        )

        self.redirect_uri = data["redirect_uri"]
        
        self.scopes = ["https://graph.microsoft.com/Mail.Send",
                       "https://graph.microsoft.com/Mail.Read",
                       "https://graph.microsoft.com/User.Read"]

    def set_service(self, args):
        url_parts = urlparse(args)
        query_parameters = parse_qs(url_parts.query)
        code = query_parameters.get('code', [None])[0]  
        result = self.app.acquire_token_by_authorization_code(
            code,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )
        self.result = result  

    def login(self):
        auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )
        webbrowser.open(auth_url)

    def get_emails(self, num_emails=10):
        try:
            access_token = self.result["access_token"]
        except KeyError:
            raise Exception("Access token is missing.")
        
        GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"
        FIELDS_TO_RETRIEVE = "id,subject,from,receivedDateTime,body,attachments"

        query_parameters = {
            "$top": num_emails,
            "$select": FIELDS_TO_RETRIEVE,
            "$expand": "attachments",
        }

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(GRAPH_API_ENDPOINT, headers=headers, params=query_parameters, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")

        email_list = []
        emails_data = response.json()["value"]
        for data in emails_data:
            from_email, to_email, subject, body, attachments = self.extract_data_from_message(data)
            email = email_util.Email(from_email, to_email, subject, body, attachments)
            email_list.append(email)
            print(emails_data)
        return email_list
    
    def get_user_email(self):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}"
        }
        try:
            response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers, timeout=30)
            response.raise_for_status()
            user_data = response.json()
            return user_data.get("mail", user_data.get("userPrincipalName", None))
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def extract_data_from_message(self, email_data):
        from_email_info = email_data.get("from", {}).get("emailAddress", {})
        from_email = from_email_info.get("address", from_email_info.get("name", None))
        to_email = self.get_user_email()
        subject = email_data["subject"]
        
        body_content_type = email_data["body"]["contentType"]
        body_content = email_data["body"]["content"]
        if body_content_type == "text":
            body_content = f"<html><body>{escape(body_content)}</body></html>"
            
        attachments = self.get_attachments(email_data)
        
        return from_email, to_email, subject, body_content, attachments

    def get_attachments(self, email_data):
        attachments = []
        if "attachments" in email_data:
            for attachment_data in email_data["attachments"]:
                if not attachment_data.get("isInline", False) and 'contentBytes' in attachment_data:
                    file_data = base64.urlsafe_b64decode(attachment_data['contentBytes'].encode('UTF-8'))
                    attachments.append({
                        'file_data': file_data,
                        'file_name': attachment_data["name"],
                        'attachment_id': attachment_data["id"]
                    })
        return attachments
    
    def draft_attachment(self,attachment):
        file_data = base64.b64encode(attachment['file_data'])
        data_body = {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'contentBytes': file_data.decode('utf-8'),
            'name': attachment['file_name'],
        }
        return data_body

    def send_email(self, email):
        to_recipients = [
            {
                'emailAddress': {
                    'address': email_address
                }
            }
            for email_address in email.to_email
        ]
        request_body = {
            'message': {
                'toRecipients': to_recipients,
                'subject': email.subject,
                'importance': 'normal',
                'body': {
                    'contentType': 'text', 
                    'content': email.body
                }
            }
        }

        if email.attachments:
            request_body['message']['attachments'] = [self.draft_attachment(attachment) for attachment in email.attachments]

        headers = {
            'Authorization': 'Bearer ' + self.result['access_token']
        }

        endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'

        try:
            response = requests.post(endpoint, headers=headers, json=request_body)
            response.raise_for_status()  # Raise an exception if request fails
            print(response.status_code)  #prints 202

            if response.status_code == 202:
                # Construct a comma-separated string of email addresses
                to_email_list = ', '.join(email.to_email)
                result_message = f"Email sent to: {to_email_list}"
            else:
                # Handle the case where the email was not sent to all recipients
                failed_recipients = ', '.join(email.to_email)
                raise Exception(f"Email not sent to: {failed_recipients}")

        except requests.exceptions.RequestException as e:
            raise Exception("An error occurred while sending the email")

        return result_message