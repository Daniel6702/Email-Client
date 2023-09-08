import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from google_auth_oauthlib.flow import Flow
import webbrowser
from flask import Flask, request
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import ssl

app = Flask(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.credentials = None
        self.service = None

        self.setWindowTitle("Google Login App")
        self.setGeometry(100, 100, 400, 200)

        login_button = QPushButton("Login with Google", self)
        login_button.setGeometry(50, 80, 100, 40)
        login_button.clicked.connect(self.login_with_google)

        send_button = QPushButton("Send Email", self)
        send_button.setGeometry(250, 80, 100, 40)
        send_button.clicked.connect(lambda: send_message(self.service,'me'))

    def login_with_google(self):
        flow = Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/gmail.send'], redirect_uri='https://localhost:8080/oauth2callback')
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
        webbrowser.open(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/gmail.send'], redirect_uri='https://localhost:8080/oauth2callback')
    flow.fetch_token(authorization_response=request.url)
    window.service = build('gmail', 'v1', credentials=flow.credentials)
    return 'Authentication successful! You can close this window.'

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {'raw': raw_message}

def send_message(service, user_id):
    message = create_message('pedersendaniel356@gmail.com', 'Subject', 'Message Body')
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("Message sent: %s" % message['id'])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile='path_to_certificate.crt', keyfile='path_to_private_key.key')

    app1 = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'threaded': True, 'ssl_context': context})
    server_thread.daemon = True
    server_thread.start()

    sys.exit(app1.exec_())