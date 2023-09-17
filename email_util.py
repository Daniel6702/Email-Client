import os
from bs4 import BeautifulSoup
import re

#Base email object
class Email:
    def __init__(self, from_email, to_email, subject, body, attachments=None):
        self.from_email = from_email
        self.to_email = to_email        #list of email adresses
        self.subject = subject
        self.body = body                #HTML or text
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
            
