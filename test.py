'''
class OutlookService():
    def __init__(self):
        self.result = None

        with open('Certificates\client_secret_outlook.json', "r") as json_file:
            data = json.load(json_file)

        authority_url = "https://login.microsoftonline.com/common"
        self.app = msal.PublicClientApplication(
            data["client_id"],
            authority=authority_url,
        )

        self.redirect_uri = data["redirect_uri"]

    def login(self):
        scopes = ["https://graph.microsoft.com/Mail.Send",
                  "https://graph.microsoft.com/Mail.Read"]
        auth_url = self.app.get_authorization_request_url(
            scopes=scopes,
            redirect_uri=self.redirect_uri,
        )
        webbrowser.open(auth_url)

    def get_emails(self):
        access_token = self.result["access_token"]

        # Make an API request to retrieve emails
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/messages"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(graph_api_endpoint, headers=headers)

        if response.status_code == 200:
            emails = response.json()
            return emails
        else:
            raise Exception(f"Failed to retrieve emails. Status code: {response.status_code}, Error: {response.text}")
        
    def send_email(self, to_email, subject, message_body, attachments=None):
        access_token = self.result["access_token"]

        # Prepare the email payload
        email_payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": message_body,
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ]
            }
        }

        # Add attachments if provided
        if attachments:
            email_payload["message"]["attachments"] = attachments

        # Make an API request to send the email
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(graph_api_endpoint, headers=headers, json=email_payload)

        if response.status_code == 202:
            return "Email sent successfully."
        else:
            raise Exception(f"Failed to send email. Status code: {response.status_code}, Error: {response.text}")



#redirect function from api
def oauth2callback_outlook(outlook_service):
    def callback():
        code = request.args['code']
        scopes = ["https://graph.microsoft.com/Mail.Send",
                  "https://graph.microsoft.com/Mail.Read"]
        result = outlook_service.app.acquire_token_by_authorization_code(
            code,
            scopes=scopes,
            redirect_uri=outlook_service.redirect_uri,
        )
        outlook_service.result = result
        return 'Authentication successful! You can close this window.'
    return callback









class GmailService():
    def __init__(self):
        self.flow = Flow.from_client_secrets_file(
            'Certificates\client_secret_google.json', 
            scopes=['https://www.googleapis.com/auth/gmail.send',
                    'https://www.googleapis.com/auth/gmail.readonly'], 
            redirect_uri='https://localhost:8080/oauth2callback'
        )
        self.service = None

    def login(self):
        authorization_url, state = self.flow.authorization_url(access_type='offline', prompt='consent')
        webbrowser.open(authorization_url)

    def set_service(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        #self.send_message('me',self.create_message('pedersendaniel356@gmail.com', 'Subject', 'Message Body'))

    def send_message(self, user_id, message):
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print("Message sent: %s" % message['id'])
        except Exception as e:
            print(f"An error occurred: {e}")   

#redirect function from api
def oauth2callback_google(gmail_service):
    def callback():
        gmail_service.flow.fetch_token(authorization_response=request.url)
        gmail_service.set_service(gmail_service.flow.credentials)
        return 'Authentication successful! You can close this window.'
    return callback

    '''