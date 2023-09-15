import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
import msal
import json
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
from base64 import b64encode


class GmailService():
    def __init__(self):
        self.flow = Flow.from_client_secrets_file(
            'Certificates\client_secret_google.json', 
            scopes=['https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.readonly'], 
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        self.service = None

    def login(self):
        authorization_url, state = self.flow.authorization_url(access_type='offline', prompt='consent')
        webbrowser.open(authorization_url)

    def set_service(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

        #temporary. get messages and print subject
        messages = self.list_messages('me', query='is:unread')
        for message in messages:
            message_data = self.get_message('me', message['id'])
            subject = None
            for header in message_data['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    print(subject)
                    break

    def send_message(self, user_id, message):
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print("Message sent: %s" % message['id'])
        except Exception as e:
            print(f"An error occurred: {e}")    

    def create_message(self,to,subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}
    
    def list_messages(self, user_id, query=''):
        try:
            response = self.service.users().messages().list(userId=user_id, q=query).execute()
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

    def login(self):
        scopes = ["https://graph.microsoft.com/Mail.Send",
                  "https://graph.microsoft.com/Mail.Read"]
        auth_url = self.app.get_authorization_request_url(
            scopes=scopes,
            redirect_uri=self.redirect_uri,
        )
        webbrowser.open(auth_url)

    def get_emails(self):
        access_token = self.result["access_token"]

        # Make an API request to retrieve emails
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/messages"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(graph_api_endpoint, headers=headers)

        if response.status_code == 200:
            emails = response.json()
            return emails
        else:
            raise Exception(f"Failed to retrieve emails. Status code: {response.status_code}, Error: {response.text}")
        
    def encode_file_to_base64(self, file_path):
        # Read the binary content of the file and convert it to base64
        with open(file_path, "rb") as file:
            file_content = file.read()
            base64_content = b64encode(file_content).decode()

        return base64_content
        
    def send_email(self, to_email, subject, message_body, attachments=None):
        access_token = self.result["access_token"]

        # Prepare the email payload
        email_payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": message_body,
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ]
            }
        }

        # Add attachments if provided
        if attachments:
            email_payload["message"]["attachments"] = attachments

        # Make an API request to send the email
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(graph_api_endpoint, headers=headers, json=email_payload)

        if response.status_code == 202:
            return "Email sent successfully."
        else:
            raise Exception(f"Failed to send email. Status code: {response.status_code}, Error: {response.text}")


