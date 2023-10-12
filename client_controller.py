import email_services
import flask_app
import threading
from time import sleep
import os
from flask import Flask, request, Response
import random
import email_util

class ClientController:
    def __init__(self, client_type, app=None):
        self.client_type = client_type
        
        # Depending on the client_type, create an instance of the corresponding email service.
        if client_type == "outlook":
            self.client = email_services.OutlookService()	
            endpoint='/oauth2callbackoutlook'
        elif client_type == "google":
            self.client = email_services.GmailService()
            endpoint='/oauth2callback'
        
        if app != None:
            app.add_endpoint(endpoint=endpoint, endpoint_name=str(random.randint(0,100)), handler=flask_app.oauth2callback(self))

        self.logged_in = False
        self.user_info = None

    #Method to initiate the login process for the selected email client.
    def login(self,user):
        self.client.login(user)
        while self.logged_in == False: #Fix this
            sleep(1)
            self.logged_in = self.client.logged_in
        else:
            if user == "new_user_saved":
                user = self.client.user
                email_util.add_user_to_file(user, 'Certificates\\users.json')

            self.on_login()    

    def send_email(self,email):
        self.client.send_email(email)

    #Emails are retrieved as a list of email objects
    def get_emails(self,folder_id=None, query="", number_of_mails = 10):
        return self.client.get_emails(folder_id,query, number_of_mails)
    
    def on_login(self):
        #x = self.client.get_email_folders()
        #email_util.print_folder_hierarchy(x)
        pass
    
    def get_email_folders(self):
        return self.client.get_email_folders()

    #Deletes the credentials 
    def delete_credentials(self):
        files_to_delete = ['Certificates/credentials.json', 'Certificates/refresh_token.txt'] 
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
    
    #Callback method to handle the response from the OAuth2 authorization process
    def api_callback(self,args):
        #Set the service using the received arguments from the redirect uri
        if not self.logged_in:
            self.client.set_service(args)