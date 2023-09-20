import client_controller
from email_util import Email, generate_attachment_dict, print_email
from datetime import datetime

if __name__ == '__main__':
    client = client_controller.ClientController("google")  #google or outlook
    client.login()

    x = input("Press enter to continue...")

    email = Email(
        from_email='me',
        to_email=['pedersendaniel3561@gmail.com',
                  'pedersendaniel356@gmail.com'],
        subject='Sample Email with Attachments',
        body='This is a sample email with attachments.',
        datetime_info = {'date': datetime.now().date(),
                         'time': datetime.now().time()},
        attachments=[
            generate_attachment_dict('Notes.txt'),
        ]
    )
    
    #client.send_email(email)

    emails = client.get_emails(5)
    for mail in emails:
        print_email(mail)
    
    