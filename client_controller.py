import email_services
import flask_app
import threading
from time import sleep
import os

class ClientController:
    def __init__(self, client_type):
        self.client_type = client_type
        
        # Depending on the client_type, create an instance of the corresponding email service.
        if client_type == "outlook":
            self.client = email_services.OutlookService()	
            endpoint='/oauth2callbackoutlook'
        elif client_type == "google":
            self.client = email_services.GmailService()
            endpoint='/oauth2callback'

        #create flask app localhost server to handle OAuth2 callback requests. Run in separate thread so rest of app can run concurrently.
        self.app = flask_app.FlaskAppWrapper('redirect_server')
        self.app.add_endpoint(endpoint=endpoint, endpoint_name='oauth2callback', handler=flask_app.oauth2callback(self))
        self.flask_thread = threading.Thread(target=self.app.run)
        self.flask_thread.start()
        
        self.logged_in = False
        self.user_info = None
        
    #Method to initiate the login process for the selected email client.
    def login(self):
        self.client.login()
        while self.logged_in == False:
            sleep(1)
            self.logged_in = self.client.logged_in
        else:
            self.on_login()    
        

    def send_email(self,email):
        self.client.send_email(email)

    #Emails are retrieved as a list of email objects
    def get_emails(self, query="", number_of_mails = 10):
        return self.client.get_emails(query, number_of_mails)
    
    def on_login(self):
        self.user_info = self.client.user_info
        
    #Deletes the credentials 
    def delete_credentials(self):
        files_to_delete = ['Certificates/credentials.json', 'Certificates/refresh_token.txt'] 
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
    
    #Callback method to handle the response from the OAuth2 authorization process
    def api_callback(self,args):
        #Set the service using the received arguments from the redirect uri
        self.client.set_service(args)
        