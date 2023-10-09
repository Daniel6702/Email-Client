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
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import time

class GmailService():
    def __init__(self):
        self.flow = Flow.from_client_secrets_file(
            'Certificates\client_secret_google.json', 
            scopes=['https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/gmail.modify',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile'], 
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        self.service = None
        self.user = None
        self.logged_in = False
        self.CREDENTIALS_FILE = 'Certificates\credentials.json'
        
    #def save_credentials(self,credentials):
    #    with open(self.CREDENTIALS_FILE, 'w') as file:
    #        file.write(credentials.to_json())

    def load_credentials(self):
        if os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, 'r') as file:
                return Credentials.from_authorized_user_file(self.CREDENTIALS_FILE)
        return None

    def login(self, user):
        if user == "new_user" or user == "new_user_saved":
            authorization_url, state = self.flow.authorization_url(access_type='offline', prompt='consent')
            webbrowser.open(authorization_url)
            return None
        else:
            credentials = Credentials.from_authorized_user_info(user.credentials)  
            if credentials.expired:
                credentials.refresh(Request())
                user.credentials = credentials.to_json()
                email_util.update_user_in_file(user, 'Certificates\\users.json')
            self.build(credentials)
            
    def build(self,credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        self.people_service = build('people', 'v1', credentials=credentials)
        self.user = self.get_user_info(credentials)
        self.logged_in = True

    def set_service(self, args):
        test_flow = Flow.from_client_secrets_file(
            'Certificates\client_secret_google.json', 
            scopes=None, #i dont know why this is needed but it is
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        test_flow.fetch_token(authorization_response=args)
        credentials = test_flow.credentials
        self.build(credentials)
        
    def get_user_info(self,credentials):
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            email = profile.get("emailAddress", None)
            people_service = self.people_service
            person = people_service.people().get(resourceName='people/me', 
                                                 personFields='names,emailAddresses').execute()
            
            name_data = person.get("names", [])[0]
            name = name_data.get("displayName", None)

            user = email_util.User(name = name, email = email, client_type="google", credentials=credentials.to_json())

            return user

        except HttpError as e:
            raise Exception(f"Request failed: {e}")
    
    def send_email(self, email):
        message = self.create_message(email)
        user_id = email.from_email
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print("Message sent: %s" % message['id'])
        except Exception as e:
            print(f"An error occurred: {e}")

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
    
    def is_html(self, text):
        tags = ['<html>', '<head>', '<body>', '<p>', '<br>', '<h1>', '<h2>', '<div>']
        return any(tag in text.lower() for tag in tags)
    
    def get_emails(self, query="in:inbox", number_of_mails = 10, includeSpamTrash = False):
        #Query Search operators you can use with Gmail: https://support.google.com/mail/answer/7190?hl=en 
        #gets a list of email id's from api. for each id get message data. extracte relevant information and attachments. create list email objects. return list
        messages = self.list_messages('me', query=query, number_of_emails=number_of_mails, includeSpamTrash = includeSpamTrash)
        email_list = []

        for message in messages:
            message_data = self.get_message('me', message['id'])
            from_email, to_email, subject, body, date_sent, attachments = self.extract_data_from_message(message_data)
            email = email_util.Email(from_email, to_email, subject, body, date_sent, attachments)
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
            
    def extract_date_and_time(self,message_data):
        headers = message_data['payload']['headers']
        date_str = next((header['value'] for header in headers if header['name'] == 'Date'), None)

        if date_str:
            date_dt = parsedate_to_datetime(date_str)
            
            time_difference_hours = 9 
            adjusted_date_dt = date_dt + timedelta(hours=time_difference_hours)
            
            date_formatted = adjusted_date_dt.strftime('%Y-%m-%d')
            time_formatted = adjusted_date_dt.strftime('%H:%M:%S.%f')
            datetime_info = {'date': date_formatted, 'time': time_formatted}
        else:
            datetime_info = {'date': None, 'time': None}
            
        return datetime_info
            
    def extract_data_from_message(self, message_data):
        headers = message_data['payload']['headers']
        from_email = next((header['value'] for header in headers if header['name'] == 'From'), None).strip()
        to_email = self.user.email
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), None)

        datetime_info = self.extract_date_and_time(message_data)

        payload = message_data.get('payload', {})
        parts = payload.get('parts', [])

        html_content = self.extract_email_content(parts)
        attachments_list = self.extract_attachments(message_data['id'], parts)

        return from_email, to_email, subject, html_content, datetime_info, attachments_list
            
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
            html_content = email_util.text_to_html(text_content)

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
        
        self.user = None
        self.logged_in = False
        self.REFRESH_TOKEN = 'Certificates\\refresh_token.txt'

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
        
        with open(self.REFRESH_TOKEN, 'w') as token_file:
            token_file.write(result.get('refresh_token'))
            
        self.logged_in = True
        self.user = self.get_user_info()

    def login(self, user):
        if user == "new_user" or user == "new_user_saved":
            auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=self.redirect_uri
            )
            webbrowser.open(auth_url)
        else:
            refresh_token = user.credentials['credentials']

            result = self.app.acquire_token_by_refresh_token(
                refresh_token=refresh_token,
                scopes=self.scopes,
            )

            if 'access_token' in result:
                self.result = result
                self.user = self.get_user_info()
                temp = {'credentials': result.get('refresh_token')}
                self.user.credentials = temp
                self.logged_in = True

            return  # Successfully logged in using refresh token
        
    def get_user_info(self):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}"
        }
        try:
            # Requesting specific fields in the API call
            response = requests.get("https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail,userPrincipalName", headers=headers, timeout=30)
            response.raise_for_status()
            user_data = response.json()

            email = user_data.get("mail", user_data.get("userPrincipalName", None))
            name = user_data.get("displayName", None)
            credentials = {'credentials': self.result.get('refresh_token')}
            user = email_util.User(name = name, email = email, client_type="outlook", credentials=credentials)

            return user
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
    

    def get_emails(self, query="", num_emails=10):
        try:
            access_token = self.result["access_token"]
        except KeyError:
            raise Exception("Access token is missing.")
        
        FIELDS_TO_RETRIEVE = "id,subject,from,receivedDateTime,body,attachments"

        # Translate the query if it's provided
        endpoint_url = "https://graph.microsoft.com/v1.0/me/messages"  # Default endpoint
        filter_query = ""

        if query:
            endpoint_url = email_util.translate_to_graph(query)
            if "$filter=" in endpoint_url:
                filter_query = endpoint_url.split("$filter=")[1]
                endpoint_url = endpoint_url.split("?")[0]

        query_parameters = {
            "$top": num_emails,
            "$select": FIELDS_TO_RETRIEVE,
            "$expand": "attachments",
        }

        if filter_query:
            query_parameters["$filter"] = filter_query

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(endpoint_url, headers=headers, params=query_parameters, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")

        email_list = []
        emails_data = response.json()["value"]
        for data in emails_data:
            from_email, to_email, subject, body, datetime_info, attachments = self.extract_data_from_message(data)
            email = email_util.Email(from_email, to_email, subject, body, datetime_info, attachments)
            email_list.append(email)
        return email_list

    def extract_data_from_message(self, email_data):
        from_email_info = email_data.get("from", {}).get("emailAddress", {})
        from_email = from_email_info.get("address", from_email_info.get("name", None)).lower()
        to_email = self.user.email
        subject = email_data["subject"]
        
        #Get body
        body_content_type = email_data["body"]["contentType"]
        body_content = email_data["body"]["content"]
        if body_content_type == "text":
            body_content = f"<html><body>{escape(body_content)}</body></html>"
        
        #Get date and time THIS DOESNT WORK
        received_datetime_str = email_data.get("receivedDateTime", None)
        if received_datetime_str:
            received_datetime_obj = datetime.fromisoformat(received_datetime_str.rstrip("Z")) + timedelta(hours=2)
            
            date_formatted = received_datetime_obj.strftime('%Y-%m-%d')
            time_formatted = received_datetime_obj.strftime('%H:%M:%S.%f')
            datetime_info = {'date': date_formatted, 'time': time_formatted}
        else:
            datetime_info = {'date': None, 'time': None}
        
        #Get attachments    
        attachments = self.get_attachments(email_data)
        
        return from_email, to_email, subject, body_content, datetime_info, attachments

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