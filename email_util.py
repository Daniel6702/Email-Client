import os
from bs4 import BeautifulSoup
import re
import html
from datetime import datetime

#Base email object
class Email:
    def __init__(self, from_email, to_email, subject, body, datetime_info, attachments=None):
        self.from_email = from_email
        self.to_email = to_email        #list of email adresses
        self.subject = subject
        self.body = body                #HTML or text
        self.datetime_info = datetime_info        #dict  datetime_info = {'date': 2023-09-18, 'time': 15:43:56.111501}. måske ændres til ISO 8601 format hvis det giver problemer
        self.attachments = attachments
'''
Attachments are stored as a list of dicts
attachment = {
            'file_data': file_data,    file data is stored as binary data 
            'file_name': file_name,
            'attachment_id': att_id
            }
'''
#Debugging method to print email contents
def print_email(email):
    print("=============================================")
    print(f"From: {email.from_email}")
    print(f"To: {email.to_email}")
    print(f"Subject: {email.subject}")
    print(f"Time and Date: {email.datetime_info['date']} {email.datetime_info['time']}")
    print("=============================================")
    if email.body:
        soup = BeautifulSoup(email.body, 'html.parser')
        body_text = soup.get_text()
        # Remove excessive line shifts and spaces
        body_text = re.sub(r'\n+', '\n', body_text).strip()
        print(body_text)
    print("=============================================")
    if email.attachments:
        print("Attachments:")
        for attachment in email.attachments:
            print(f"- {attachment['file_name']}")
    print("=============================================")
    
#Convert binary data back to a file and save it to the specified path
def save_attachment(file_data, path, file_name): 
    file_path = os.path.join(path, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_data)
        
#Convert a file to binary data and create attachment dict 
def generate_attachment_dict(file_path): 
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'rb') as file:
        file_data = file.read()

    file_name = os.path.basename(file_path)

    attachment_dict = {
        'file_data': file_data,
        'file_name': file_name,
    }
    return attachment_dict

#convert/integrate text into html
def text_to_html(text):
    escaped_text = html.escape(text)
    return f"""
            <!DOCTYPE html>
            <html>
            <body>
                <p>{escaped_text}</p>
            </body>
            </html>
            """
#  Compare two HTML snippets to determine if they would visually appear the samewhen rendered- It won't work for all scenarios.
def visually_similar(html1, html2):

    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')

    text1 = ' '.join(soup1.stripped_strings)
    text2 = ' '.join(soup2.stripped_strings)

    return text1 == text2

#Generate a dummy email for testing purposes
def get_test_email(client_type):
    if client_type == "outlook":
        dummy_email = Email(
        from_email='dacasoftdev_test@hotmail.com',
        to_email=['dacasoftdev_test@hotmail.com'],
        subject='Sample Email with Attachments',
        body='This is a sample email with attachments.',
        datetime_info = {'date': str(datetime.now().date()),
                         'time': str(datetime.now().time())},
        attachments=[
            generate_attachment_dict('Notes.txt'),
        ]
        )
    elif client_type == "google":
        dummy_email = Email(
        from_email='dacasoftdev.test@gmail.com',
        to_email=['dacasoftdev.test@gmail.com'], 
        subject='Sample Email with Attachments',
        body='This is a sample email with attachments.',
        datetime_info = {'date': str(datetime.now().date()),
                         'time': str(datetime.now().time())},
        attachments=[
            generate_attachment_dict('Notes.txt'),
        ]
        )
    return dummy_email
            
