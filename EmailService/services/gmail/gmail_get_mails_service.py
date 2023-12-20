import html
import base64
from email.utils import parsedate_to_datetime
from datetime import timedelta
import logging
import re
from datetime import datetime, timedelta

from ..service_interfaces import GetMailsService
from ...util import GmailSession 
from ...models import Folder, Filter, Email

class GmailGetMailsService(GetMailsService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service
        self.page_tokens = {1: None}  

    def get_mails(self, folder: Folder = Folder("", "INBOX", []), query: str = "", max_results: int = 10, page_number: int = 1) -> list[Email]:
        page_token = self.page_tokens.get(page_number)

        if folder.id == "":
            query = f' {query}'
        else:
            query = f' {query} label:{folder.id}'

        try:
            response = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results, 
                includeSpamTrash=False, pageToken=page_token
            ).execute()
            messages = response.get('messages', [])
            logging.info("Successfully retrieved email ids from Gmail")

            nextPageToken = response.get('nextPageToken', None)
            if nextPageToken:
                self.page_tokens[page_number + 1] = nextPageToken

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        email_list = []
        for message in messages:
            message_data = self.get_message_data('me', message['id'])
            email = Email(*self.extract_data_from_message(message_data), folder=folder)
            email_list.append(email)
        logging.info("Successfully parsed email data from Gmail")

        return email_list
    
    def get_page_token(self, page_number):
        if page_number in self.page_tokens:
            return self.page_tokens[page_number]

        current_page = max(self.page_tokens.keys())
        while current_page < page_number:
            current_page += 1
            response = self.service.users().messages().list(
                userId='me', maxResults=10, pageToken=self.page_tokens[current_page - 1]
            ).execute()

            self.page_tokens[current_page] = response.get('nextPageToken')

            if not self.page_tokens[current_page]:
                break

        return self.page_tokens.get(page_number)
        
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
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body'].get('attachmentId', '')
                    if att_id:
                        att = self.service.users().messages().attachments().get(userId='me', messageId=message_id, id=att_id).execute()
                        data = getattr(att, 'data', '')
                    else:
                        continue

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
    
    def construct_query(self, user_query: str) -> str:
        from_pattern = re.compile(r"from:(\S+)")
        to_pattern = re.compile(r"to:(\S+)")
        subject_pattern = re.compile(r"subject:(\S+)")

        query_parts = [f'({user_query})']

        if from_match := from_pattern.search(user_query):
            query_parts.append(f'from:{from_match.group(1)}')

        if to_match := to_pattern.search(user_query):
            query_parts.append(f'to:{to_match.group(1)}')

        if subject_match := subject_pattern.search(user_query):
            query_parts.append(f'subject:{subject_match.group(1)}')

        date_pattern = re.compile(r"date:(\d{4}-\d{2}-\d{2})")
        if date_match := date_pattern.search(user_query):
            date_str = date_match.group(1)
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                next_day = date + timedelta(days=1)
                query_parts.append(f'after:{date.strftime("%Y/%m/%d")} before:{next_day.strftime("%Y/%m/%d")}')
            except ValueError:
                pass 

        combined_query = ' '.join(query_parts)
        return combined_query
    
    def construct_filter_query(self, filter: Filter) -> str:
        query_parts = []

        if filter.before_date:
            query_parts.append(f"before:{filter.before_date.strftime('%Y/%m/%d')}")
        if filter.after_date:
            query_parts.append(f"after:{filter.after_date.strftime('%Y/%m/%d')}")
        if filter.from_email:
            query_parts.append(f"from:{filter.from_email}")
        if filter.to_email:
            query_parts.append(f"to:{filter.to_email}")
        if filter.is_read is not None:
            query_parts.append("is:unread" if not filter.is_read else "is:read")
        if filter.has_attachment:
            query_parts.append("has:attachment")
        if filter.contains:
            for item in filter.contains:
                query_parts.append(f'"{item}"')
        if filter.not_contains:
            for item in filter.not_contains:
                query_parts.append(f'-"{item}"')

        return ' '.join(query_parts)
    
    def search(self, query: str, max_results: int = 10) -> list[Email]:
        search_query = self.construct_query(query)
        return self.get_mails(folder=Folder("","",[]),query=search_query, max_results=max_results)
    
    def filter(self, filter: Filter, max_results: int = 10) -> list[Email]:
        filter_query = self.construct_filter_query(filter)
        return self.get_mails(folder=filter.folder, query=filter_query, max_results=max_results)
    
    def search_filter(self, search_query: str, filter: Filter, max_results: int = 10) -> list[Email]:
        search_result = self.search(search_query, max_results)
        search_result_ids = {email.id for email in search_result}

        filter_result = self.filter(filter, max_results)
        filter_result_ids = {email.id for email in filter_result}

        common_ids = search_result_ids.intersection(filter_result_ids)
        combined_emails = [email for email in search_result if email.id in common_ids]
        return combined_emails
