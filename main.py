import client_controller
from email_util import Email, generate_attachment_dict, print_email

if __name__ == '__main__':
    client = client_controller.ClientController("outlook")  #google or outlook
    client.login()

    x = input("Press enter to continue...")

    email = Email(
        from_email='me',
        to_email=['pedersendaniel3561@gmail.com',
                  'pedersendaniel356@gmail.com'],
        subject='Sample Email with Attachments',
        body='This is a sample email with attachments.',
        attachments=[
            generate_attachment_dict('requirements.txt'),
        ]
    )
    
    client.send_email(email)

    emails = client.get_emails(10)
    for mail in emails:
        print_email(mail)
    
    