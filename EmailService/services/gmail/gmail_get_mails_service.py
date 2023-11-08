from email_util import Email, text_to_html
import base64
from email.utils import parsedate_to_datetime
from datetime import timedelta

from ..service_interfaces import GetMailsService
from ...util import GmailSession 

class GmailGetMailsService(GetMailsService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def get_mails(self, folder_id: str ='INBOX', query: str = "", max_results: int = 10) -> list[Email]:
        query = f'in:{folder_id} {query}'
        #Returns a list of messages from the given folder and query
        try:
            response = self.service.users().messages().list(userId='me', q=query, maxResults = max_results, includeSpamTrash = False).execute()
            messages = response.get('messages', [])
        except Exception as e:
            return []
            print(f"An error occurred: {e}")

        #Extracts the data from each message and returns a list of Email objects
        email_list = []
        for message in messages:
            message_data = self.get_message_data('me', message['id'])
            from_email, to_email, subject, body, date_sent, attachments = self.extract_data_from_message(message_data)
            email = Email(from_email=from_email, 
                          to_email=to_email, 
                          subject=subject, 
                          body=body, 
                          datetime_info=date_sent, 
                          attachments=attachments, 
                          id=message['id'])
            email_list.append(email)

        return email_list
    
    def get_message_data(self, user_id, message_id):
        try:
            message = self.service.users().messages().get(userId=user_id, id=message_id).execute()
            return message
        except Exception as e:
            print(f"An error occurred: {e}")
               
    def extract_date_and_time(self, message_data):
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
        to_email = None
        for header in headers:
            if header['name'].lower() == 'to':
                to_email = header['value']
                break

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
            html_content = text_to_html(text_content)

        return html_content

    def extract_attachments(self, message_id, parts):
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