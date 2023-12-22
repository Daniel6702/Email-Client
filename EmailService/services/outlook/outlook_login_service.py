import webbrowser
import threading
from flask import request
import msal
import json
from urllib.parse import urlparse, parse_qs
import logging

from flask_app import FlaskAppWrapper
from ...util import OutlookSession
from ..service_interfaces import LoginService
from ...models import User

class OutlookLoginService(LoginService):
    session = OutlookSession(result=None,credentials=None)
    login_event = threading.Event()

    def __init__(self, client_secret_path: str = 'Certificates\\client_secret_outlook.json'):
        with open(client_secret_path, "r") as json_file:
            data = json.load(json_file)

        self.app = msal.PublicClientApplication(data["client_id"],authority="https://login.microsoftonline.com/common")
        self.scopes = [
            "https://graph.microsoft.com/Mail.Send",
            "https://graph.microsoft.com/Mail.Read",
            "https://graph.microsoft.com/Mail.ReadWrite",
            "https://graph.microsoft.com/User.Read",
            "https://graph.microsoft.com/Contacts.Read",
            "https://graph.microsoft.com/Contacts.ReadWrite",
            "https://graph.microsoft.com/MailboxSettings.ReadWrite"  # Added scope
        ]
        self.redirect_uri = data["redirect_uri"]

    def new_login(self):
        logging.info("Starting Outlook login process")
        self.flask_app = FlaskAppWrapper('redirect_server')
        self.flask_app.add_endpoint(endpoint='/oauth2callbackoutlook', 
                         endpoint_name='outlook_callback', 
                         handler=self.outlook_login_process_callback()) 
               
        authorization_url = self.app.get_authorization_request_url(scopes=self.scopes,redirect_uri=self.redirect_uri)
        print(authorization_url)
        webbrowser.open(authorization_url)

    def login_user(self, user: User):
        logging.info(f"Starting Outlook login process for user {user.email}")
        refresh_token = user.credentials['credentials']
        result = self.app.acquire_token_by_refresh_token(refresh_token=refresh_token,scopes=self.scopes,)
        if 'access_token' in result:
            self.session.result = result
            self.session.credentials = {'credentials': result.get('refresh_token')}    
            logging.info(f"Successfully logged in user {user.email}") 
            self.login_event.set()

    def outlook_login_process_callback(self):
        def callback():
            self.callback_handler(request.url)
            return 'Authentication successful! You can close this window.'
        return callback

    def callback_handler(self,args):
        url_parts = urlparse(args)
        query_parameters = parse_qs(url_parts.query)
        code = query_parameters.get('code', [None])[0]  
        result = self.app.acquire_token_by_authorization_code(code,scopes=self.scopes,redirect_uri=self.redirect_uri,)
        self.session.result = result
        self.session.credentials = {'credentials': result.get('refresh_token')}  
        logging.info(f"Successfully logged in")   
        self.login_event.set()

    def get_session(self):
        return self.session