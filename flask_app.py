from flask import Flask, request, Response
import ssl
import threading
import sys
import time
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

class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run      
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile='Certificates/certificate.crt', keyfile='Certificates/private_key.key')
        self.app = Flask(name)
        self.flask_thread = thread_with_trace(target=self.run)  
        self.flask_thread.start()

    def run(self, host='0.0.0.0', port=2550):
        self.app.run(host=host, port=port, threaded=True, ssl_context=self.context)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def shutdown(self):
        if self.flask_thread.is_alive():
            self.flask_thread.kill()
            time.sleep(1)
            self.flask_thread.join()
            print("Flask thread killed")
 