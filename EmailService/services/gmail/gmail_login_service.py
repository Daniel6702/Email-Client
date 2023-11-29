from ...models import User
#from EmailService.models.user import User

from flask_app import FlaskAppWrapper
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from webbrowser import open
import threading
from flask import request
import logging

from ...util import GmailSession
from ..service_interfaces import LoginService

class GmailLoginService(LoginService):
    session = GmailSession(gmail_service=None, people_service=None, credentials=None)
    login_event = threading.Event()

    def new_login(self):
        logging.info("Starting Gmail login process")
        app = FlaskAppWrapper('redirect_server')
        app.add_endpoint(endpoint='/oauth2callback', 
                         endpoint_name='gmail_callback', 
                         handler=self.gmail_login_process_callback())
        flow = Flow.from_client_secrets_file(
            'Certificates\\client_secret_google.json', 
            scopes=['https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/gmail.modify',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/contacts',
                    'https://www.googleapis.com/auth/gmail.settings.basic'], 
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
        open(authorization_url)

    def gmail_login_process_callback(self):
        def callback():
            self.callback_handler(request.url)
            return 'Authentication successful! You can close this window.'
        return callback

    def callback_handler(self,args):
        flow = Flow.from_client_secrets_file(
            'Certificates\\client_secret_google.json', 
            scopes=None,
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        flow.fetch_token(authorization_response=args)
        credentials = flow.credentials
        self.build_service(credentials)

    def login_user(self, user: User):
        logging.info(f"Starting Gmail login process for user {user.email}")
        credentials = Credentials.from_authorized_user_info(user.credentials)
        if credentials.expired:
            try:
                credentials.refresh(Request())
            except Exception as refresh_error:
                logging.error(f"Error refreshing credentials for user {user.email}: {refresh_error}")
                self.new_login()
        self.build_service(credentials)

    def build_service(self,credentials):
        self.session.credentials = credentials
        self.session.gmail_service = build('gmail', 'v1', credentials=credentials)
        self.session.people_service = build('people', 'v1', credentials=credentials)
        logging.info(f"Successfully logged in")
        self.login_event.set()

    def get_session(self):
        return self.session