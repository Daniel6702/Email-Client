import client_controller
from email_util import Email, generate_attachment_dict, print_email
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from UI import MainWindow
import flask_app
from UI import LoginScreen

if __name__ == '__main__':
    app = flask_app.FlaskAppWrapper('redirect_server')
    client = client_controller.ClientController("outlook", app)  # google or outlook
    client.login()

    app = QApplication(sys.argv)
    login_screen = LoginScreen()  # Create a LoginScreen instance
    html_container = [None]  # Use a list to store the html variable

    def on_login_successful():
        html = html_container[0]  # Retrieve the html from the container
        #After successful login, fetch emails and create MainWindow
        emails = client.get_emails(number_of_mails=1)
        for mail in emails:
            print_email(mail)
            html = mail.body
        html_container[0] = html  # Update the html in the container

        # Create the MainWindow and show it
        window = MainWindow(html)
        window.show()

    #Connect the login_successful signal to the on_login_successful slot
    login_screen.login_successful.connect(MainWindow.on_login_successful)

    # Show the LoginScreen
    login_screen.show()

    sys.exit(app.exec_())
