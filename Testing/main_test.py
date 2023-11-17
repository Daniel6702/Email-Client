import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
from EmailService.models.email_client import EmailClient
from EmailService.factories.gmail_service_factory import GmailServiceFactory
from EmailService.factories.outlook_service_factory import OutlookServiceFactory
from EmailService.models import User, Email
from user_manager import UserDataManager
import json
from datetime import datetime
import time
from html.parser import HTMLParser

user_manager = UserDataManager('Testing\\test_users.bin')
with open('Testing\\test_users.json', 'r') as f:
    users = json.load(f)

gmail_user = User.from_dict(users[0])
gmail_client = EmailClient(GmailServiceFactory(), user_manager)
gmail_client.login(gmail_user, False)

outlook_user = User.from_dict(users[1])
outlook_client = EmailClient(OutlookServiceFactory(), user_manager)
outlook_client.login(outlook_user, False)

mock_outlook_email = Email(from_email=outlook_user.email,
                   to_email=[outlook_user.email],
                   subject='Test Email',
                   body='This is a test email',
                   datetime_info = {'date': str(datetime.now().date()),
                                    'time': str(datetime.now().time())},
                   attachments=[],
                   id=None,
                   is_read=False)

mock_gmail_email = Email(from_email=gmail_user.email,
                   to_email=[gmail_user.email],
                   subject='Test Email',
                   body='This is a test email',
                   datetime_info = {'date': str(datetime.now().date()),
                                    'time': str(datetime.now().time())},
                   attachments=[],
                   id=None,
                   is_read=False)

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return "".join(self.result)

def extract_text_from_html(html):
    parser = HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()

def compare_emails(sent_email, received_email):
    mismatches = []

    if sent_email.from_email != received_email.from_email:
        mismatches.append(f"Sender mismatch: sent '{sent_email.from_email}', received '{received_email.from_email}'")

    if sent_email.to_email[0] != received_email.to_email:
        mismatches.append(f"Recipients mismatch: sent '{sent_email.to_email[0]}', received '{received_email.to_email}'")

    if sent_email.subject != received_email.subject:
        mismatches.append(f"Subject mismatch: sent '{sent_email.subject}', received '{received_email.subject}'")

    sent_body_text = extract_text_from_html(sent_email.body)
    received_body_text = extract_text_from_html(received_email.body)
    
    if sent_body_text.strip() != received_body_text.strip():
        mismatches.append("Body content mismatch")

    return mismatches

gmail_client.send_mail(mock_gmail_email)
outlook_client.send_mail(mock_outlook_email)
time.sleep(5)
received_outlook_email = outlook_client.get_mails(folder_id="", query="",max_results=1)[0]
received_gmail_email = gmail_client.get_mails(folder_id="", query="",max_results=1)[0]

print(mock_gmail_email)
print(received_gmail_email)
print("\n")
print(mock_outlook_email)
print(received_outlook_email)

mismatches1 = compare_emails(mock_gmail_email, received_gmail_email)
mismatches2 = compare_emails(mock_outlook_email, received_outlook_email)

if mismatches1:
    print("Differences found:")
    for mismatch in mismatches1:
        print(mismatch)

print("\n")

if mismatches2:
    print("Differences found:")
    for mismatch in mismatches2:
        print(mismatch)

if not mismatches1 and not mismatches2:
    print("TEST PASSED")