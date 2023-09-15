import email_services
import flask_app

if __name__ == '__main__':
    gmail_service = email_services.GmailService()
    gmail_service.login()

    outlook_service = email_services.OutlookService()
    outlook_service.login()

    app = flask_app.FlaskAppWrapper('redirect_server')
    app.add_endpoint(endpoint='/oauth2callback', endpoint_name='oauth2callback', handler=flask_app.oauth2callback_google(gmail_service))
    app.add_endpoint(endpoint='/oauth2callbackoutlook', endpoint_name='oauth2callbackoutlook', handler=flask_app.oauth2callback_outlook(outlook_service))
    app.run()
