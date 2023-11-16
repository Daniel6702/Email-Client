import html
from ...models import Email
import base64
from email.utils import parsedate_to_datetime
from datetime import timedelta
import logging
from typing import List, Generator
from googleapiclient.errors import HttpError

from ..service_interfaces import GetMailsService
from ...util import GmailSession 

class GmailGetMailsService(GetMailsService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service
    '''
    def get_mails(self, folder_id: str ='INBOX', query: str = "", max_results: int = 10) -> Generator[Email, None, None]: #Test for improving loading time
        query = f'in:{folder_id} {query}'
        try:
            response = self.service.users().messages().list(userId='me', q=query, maxResults=max_results, includeSpamTrash=False).execute()
            messages = response.get('messages', [])
            logging.info("Successfully retrieved email ids from Gmail")
        except HttpError as e:
            logging.error(f"Failed to retrieve emails: {e}")
            raise

        for message in messages:
            try:
                message_data = self.get_message_data('me', message['id'])
                yield Email(*self.extract_data_from_message(message_data))
            except HttpError as e:
                logging.error(f"Error processing message {message['id']}: {e}")

        logging.info("Successfully parsed email data from Gmail")
    '''

    def get_mails(self, folder_id: str ='INBOX', query: str = "", max_results: int = 10) -> list[Email]:
        query = f'in:{folder_id} {query}'
        try:
            response = self.service.users().messages().list(userId='me', q=query, maxResults = max_results, includeSpamTrash = False).execute()
            messages = response.get('messages', [])
            logging.info(f"Successfully retrieved email id's from Gmail")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"Request failed: {e}")    

        email_list = []
        for message in messages:
            message_data = self.get_message_data('me', message['id'])
            email = Email(*self.extract_data_from_message(message_data))
            email_list.append(email)
        logging.info(f"Successfully parsed email data from Gmail")
        return email_list
        
    def get_message_data(self, user_id: str, message_id: str) -> dict:
        try:
            message = self.service.users().messages().get(userId=user_id, id=message_id).execute()
            return message
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"Request failed: {e}")
        
    def extract_data_from_message(self, message_data: dict) -> tuple:
        from_email = self.extract_sender(message_data)
        to_email = self.extract_recipient(message_data)
        subject = self.extract_subject(message_data)
        is_read = self.extract_is_read(message_data)
        datetime_info = self.extract_date_and_time(message_data)
        content = self.extract_email_content(message_data)
        attachments_list = self.extract_attachments(message_data)
        id = message_data['id']
        return from_email, to_email, subject, content, datetime_info, attachments_list, id, is_read
        
    def extract_recipient(self, message_data: dict) -> str:
        headers = message_data['payload']['headers']
        to_email = None
        for header in headers:
            if header['name'].lower() == 'to':
                to_email = header['value']
                break
        return to_email
        
    def extract_sender(self, message_data: dict) -> str:
        headers = message_data['payload']['headers']
        return next((header['value'] for header in headers if header['name'] == 'From'), None).strip()
         
    
    def extract_subject(self, message_data: dict) -> str:
        headers = message_data['payload']['headers']
        return next((header['value'] for header in headers if header['name'].lower() == 'subject'), None)
               
    def extract_date_and_time(self, message_data: dict) -> dict:
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
    
    def extract_is_read(self, message_data: dict) -> bool:
        return 'UNREAD' not in message_data.get('labelIds', [])
            
    def extract_email_content(self, message_data: dict) -> str:
        payload = message_data.get('payload', {})
        parts = payload.get('parts', [])
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
            html_content = self.text_to_html(text_content)

        return html_content

    def extract_attachments(self, message_data: dict) -> list[dict]:
        message_id = message_data['id']
        payload = message_data.get('payload', {})
        parts = payload.get('parts', [])
        attachments_list = []

        for part in parts:
            if part['filename']:  
                mimeType = part.get('mimeType', '')

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
    
    def text_to_html(self,text):
        escaped_text = html.escape(text)
        return f"""
                <!DOCTYPE html>
                <html>
                <body>
                    <p>{escaped_text}</p>
                </body>
                </html>
                """
    



    

    