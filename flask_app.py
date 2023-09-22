from flask import Flask, request, Response
import ssl
import threading

#This function acts as a wrapper for OAuth2 authentication callback requests. 
#It is called when the user has successfully logged in to the email service.
#The request.url argument is used to retrieve the access token and create a service that can be used to access the email account.
def oauth2callback(client):
    def callback():
        client.api_callback(request.url)
        return 'Authentication successful! You can close this window.'
    return callback

class EndpointAction(object):
    def __init__(self, action):
        self.action = action
    #When instance is called by Flask, the action method is called
    def __call__(self, *args):
        return self.action(*args)

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        # Initialize SSL context with certificate data for HTTPS requests
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile='Certificates\certificate.crt', keyfile='Certificates\private_key.key')
        self.app = Flask(name)
        self.flask_thread = threading.Thread(target=self.run)
        self.flask_thread.start()

    #Run the Flask app with given host and port, and with SSL
    def run(self, host='0.0.0.0', port=8080):
        self.app.run(host=host, port=port, threaded=True, ssl_context=self.context)

    #Add a new URL rule to the Flask app. The handler is the method to be called when the endpoint is accessed.
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))