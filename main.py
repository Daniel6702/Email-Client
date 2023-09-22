import client_controller
from email_util import Email, generate_attachment_dict, print_email
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from UI import MainWindow
import flask_app

if __name__ == '__main__':
    app = flask_app.FlaskAppWrapper('redirect_server')
    client = client_controller.ClientController("outlook",app)  #google or outlook
    client.login()
    
    #emails = client.get_emails(query="from:pedersendaniel3561@gmail.com has:attachment after:2023/09/19",number_of_mails=5)
    emails = client.get_emails(number_of_mails=1)
    html = None
    for mail in emails:
        print_email(mail)
        html = mail.body

    app = QApplication(sys.argv)
    window = MainWindow(html)
    sys.exit(app.exec_())
    
    