from ..service_interfaces import GetMailsService
from ...util import OutlookSession 
from ...models import Email
import requests
import base64
from datetime import datetime, timedelta
from html import escape
import logging

class OutlookGetMailsService(GetMailsService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def get_mails(self, folder_id: str, query: str, max_results: int = 10) -> list[Email]:
        try:
            access_token = self.result["access_token"]
        except KeyError:
            raise Exception("Access token is missing.")
        
        FIELDS_TO_RETRIEVE = "id,subject,from,receivedDateTime,body,attachments"

        if folder_id:
            endpoint_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"
        else:
            endpoint_url = "https://graph.microsoft.com/v1.0/me/messages" 

        filter_query = ""

        if query:
            endpoint_url, filter_query = self.translate_to_graph(query, base_endpoint=endpoint_url)

        query_parameters = {
            "$top": max_results,
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
            logging.info(f"Successfully retrieved email data from Outlook")

        except requests.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"Request failed: {e}")

        email_list = []
        emails_data = response.json()["value"]
        for data in emails_data:
            from_email, to_email, subject, body, datetime_info, attachments, email_id, is_read = self.extract_data_from_message(data)
            email = Email(from_email, to_email, subject, body, datetime_info, attachments, id=email_id, is_read=is_read)
            email_list.append(email)
        logging.info(f"Successfully parsed email data from Outlook")
        return email_list 

    def extract_data_from_message(self, email_data: dict) -> tuple[str, str, str, str, dict, list[dict], str]:
        from_email_info = email_data.get("from", {}).get("emailAddress", {})
        from_email = from_email_info.get("address", from_email_info.get("name", None))
        if from_email:
            from_email.lower()
        to_recipients_info = email_data.get("toRecipients", [])
        to_emails = [recipient.get("emailAddress", {}).get("address", "").lower() for recipient in to_recipients_info]
        if to_emails and len(to_emails) > 0:
            to_email = to_emails[0]
        else:
            to_email = None
        is_read = email_data.get("isRead", False)

        subject = email_data["subject"]
        email_id = email_data['id']
        
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
        
        return from_email, to_email, subject, body_content, datetime_info, attachments, email_id, is_read

    def get_attachments(self, email_data: dict) -> list[dict]:
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
    

    def translate_to_graph(self,query, base_endpoint="https://graph.microsoft.com/v1.0/me/messages"):
        parts = query.split()
        translated_parts = []
        folder_endpoint = base_endpoint 

        for part in parts:
            if part.startswith("from:"):
                email = part.split("from:")[1]
                translated_parts.append(f"from/emailAddress/address eq '{email}'")
            elif part == "is:unread":
                translated_parts.append("isRead eq false")
            elif part == "is:read":
                translated_parts.append("isRead eq true")
            elif part == "has:attachment":
                translated_parts.append("hasAttachments eq true")
            elif part == "label:important":
                translated_parts.append("importance eq 'high'")
            elif part.startswith("after:"):
                date = part.split("after:")[1].replace('/', '-')
                translated_parts.append(f"receivedDateTime ge {date}T11:59:59Z")
            elif part.startswith("before:"):
                date = part.split("before:")[1].replace('/', '-')
                translated_parts.append(f"receivedDateTime lt {date}T11:59:59Z")
            elif part == "in:trash":
                folder_endpoint = "https://graph.microsoft.com/v1.0/me/mailFolders/deleteditems/messages"
            elif part == "in:spam":
                folder_endpoint = "https://graph.microsoft.com/v1.0/me/mailFolders/junkemail/messages"

            #... (rest of your conditions)
            # No changes needed in the conditions

        # If there's any filtering to be done on top of the folder selection:
        if translated_parts:
            filter_query = "$filter=" + " and ".join(translated_parts)
            return folder_endpoint, filter_query
        else:
            return folder_endpoint, ""