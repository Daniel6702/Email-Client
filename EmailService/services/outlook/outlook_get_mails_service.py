from ..service_interfaces import GetMailsService
from ...util import OutlookSession 
import requests
import base64
from datetime import datetime, timedelta
from html import escape
import logging
import re
from ...models import Folder, Filter, Email

class OutlookGetMailsService(GetMailsService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def get_mails(self, folder: Folder = Folder("", None, []), query: str = "", max_results: int = 10, page_number: int = 1) -> list[Email]:
        folder_id = folder.id
        
        try:
            access_token = self.result["access_token"]
        except KeyError:
            raise Exception("Access token is missing.")

        FIELDS_TO_RETRIEVE = "id,subject,from,receivedDateTime,body,attachments,isRead"

        base_url = "https://graph.microsoft.com/v1.0/me"
        endpoint_url = f"{base_url}/mailFolders/{folder_id}/messages" if folder_id else f"{base_url}/messages"

        skip_count = (page_number - 1) * max_results

        query_parameters = {
            "$top": max_results,
            "$skip": skip_count,
            "$select": FIELDS_TO_RETRIEVE,
            "$expand": "attachments"
        }

        if query:
            query_parameters = {
                "$top": max_results,
                "$select": FIELDS_TO_RETRIEVE,
                "$expand": "attachments"
            }
            if query.startswith('search:'):
                query_parameters["$search"] = query[len('search:'):]
            elif query.startswith('filter:'):
                query_parameters["$filter"] = query[len('filter:'):] 
        else:
            query_parameters = {
                "$top": max_results,
                "$skip": skip_count,
                "$select": FIELDS_TO_RETRIEVE,
                "$expand": "attachments"
            }

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(endpoint_url, headers=headers, params=query_parameters, timeout=30)
            response.raise_for_status()
            data = response.json()
            emails = [Email(*self.extract_data_from_message(item)) for item in data.get('value', [])]

            return emails
        except requests.RequestException as e:
            logging.error(f"Request failed: {e.response.text}")
            raise Exception(f"Request failed: {e}")

    def extract_data_from_message(self, email_data: dict) -> tuple[str, str, str, str, dict, list[dict], str]:
        from_email = self.extract_from_email(email_data)
        to_email = self.extract_to_email(email_data)
        subject = email_data["subject"]
        email_id = email_data['id']
        is_read = email_data.get("isRead", False)
        datetime_info = self.extract_date_and_time(email_data)
        body_content = self.extract_email_content(email_data)
        attachments = self.extract_attachments(email_data)
        return from_email, to_email, subject, body_content, datetime_info, attachments, email_id, is_read

    def extract_attachments(self, email_data: dict) -> list[dict]:
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
    
    def extract_from_email(self, email_data: dict) -> str:
        from_email = email_data.get("from", {}).get("emailAddress", {}).get("address", None)
        if from_email:
            from_email = from_email.lower()
        return from_email
    
    def extract_to_email(self, email_data: dict) -> str:
        to_recipients_info = email_data.get("toRecipients", [])
        to_emails = [recipient.get("emailAddress", {}).get("address", "") for recipient in to_recipients_info]
        if to_emails and len(to_emails) > 0:
            return to_emails[0]
        else:
            return None
        
    def extract_date_and_time(self, email_data: dict) -> dict:
        received_datetime_str = email_data.get("receivedDateTime", None)
        if received_datetime_str:
            received_datetime_obj = datetime.fromisoformat(received_datetime_str.rstrip("Z"))
            received_datetime_obj += timedelta(hours=1)
            date_formatted = received_datetime_obj.strftime('%Y-%m-%d')
            time_formatted = received_datetime_obj.strftime('%H:%M:%S.%f')
            datetime_info = {'date': date_formatted, 'time': time_formatted}
        else:
            datetime_info = {'date': None, 'time': None}
        return datetime_info
    
    def extract_email_content(self, email_data: dict) -> str:
        body_content_type = email_data["body"]["contentType"]
        body_content = email_data["body"]["content"]
        if body_content_type == "text":
            body_content = f"<html><body>{escape(body_content)}</body></html>"
        return body_content
    
    def create_filter_query(self, filter: Filter) -> str:
        conditions = []

        if filter.before_date:
            formatted_before_date = filter.before_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            conditions.append(f"receivedDateTime lt {formatted_before_date}")
        if filter.after_date:
            formatted_after_date = filter.after_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            conditions.append(f"receivedDateTime ge {formatted_after_date}")
        if filter.from_email:
            conditions.append(f"from/emailAddress/address eq '{filter.from_email}'")
        if filter.to_email:
            conditions.append(f"toRecipients/any(t:t/emailAddress/address eq '{filter.to_email}')")
        if filter.is_read is not None:
            read_value = 'true' if filter.is_read else 'false'
            conditions.append(f"isRead eq {read_value}")
        if filter.has_attachment is not None:
            attachment_value = 'true' if filter.has_attachment else 'false'
            conditions.append(f"hasAttachments eq {attachment_value}")
        if filter.contains:
            for item in filter.contains:
                conditions.append(f"(contains(subject, '{item}') or contains(body/content, '{item}'))")
        if filter.not_contains:
            for item in filter.not_contains:
                conditions.append(f"(not contains(subject, '{item}') and not contains(body/content, '{item}'))")

        return " and ".join(conditions)
        
    def search(self, query: str, max_results: int = 10) -> list[Email]:
        query = f'search:"{query}"'
        emails = self.get_mails(folder=Folder("", None, []), query=query, max_results=max_results)
        return emails
    
    def filter(self, filter: Filter, max_results: int = 10) -> list[Email]:
        filter_query = f'filter:{self.create_filter_query(filter)}' 
        emails = self.get_mails(folder=filter.folder, query=filter_query, max_results=max_results)
        return emails
    
    def search_filter(self, search_query: str, filter_obj: Filter, max_results: int = 10) -> list[Email]:
        search_result = self.search(search_query, max_results)
        search_result_ids = {email.id for email in search_result}

        filter_result = self.filter(filter_obj, max_results)
        filter_result_ids = {email.id for email in filter_result}

        common_ids = search_result_ids.intersection(filter_result_ids)
        combined_emails = [email for email in search_result if email.id in common_ids]

        return combined_emails