from flask import Flask, request, Response
import ssl

def oauth2callback_google(gmail_service):
    def callback():
        gmail_service.flow.fetch_token(authorization_response=request.url)
        gmail_service.set_service(gmail_service.flow.credentials)
        return 'Authentication successful! You can close this window.'
    return callback

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
        outlook_service.send_email("pedersendaniel3561@gmail.com","hello",'test')
        print(outlook_service.get_emails())
        return 'Authentication successful! You can close this window.'
    return callback

class EndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action(*args)

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile='Certificates\certificate.crt', keyfile='Certificates\private_key.key')
        self.app = Flask(name)

    def run(self, host='0.0.0.0', port=8080):
        self.app.run(host=host, port=port, threaded=True, ssl_context=self.context)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))