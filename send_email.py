import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from google_auth_oauthlib.flow import Flow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Login App")
        self.setGeometry(100, 100, 400, 200)

        login_button = QPushButton("Login with Google", self)
        login_button.setGeometry(150, 80, 150, 40)
        login_button.clicked.connect(self.login_with_google)

    def login_with_google(self):
        flow = Flow.from_client_secrets_file('client_secret_292747207172-ji8kc1isegb95v08bdo62bnu19a8gk3m.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/gmail.send'], redirect_uri='http://localhost:8080/oauth2callback')
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')

        # Open the authorization URL in a browser window
        import webbrowser
        webbrowser.open(authorization_url)

        # Once the user has logged in and granted permissions, handle the callback URL
        # and exchange the authorization code for tokens
        callback_url = input("Enter the callback URL after login: ")
        flow.fetch_token(authorization_response=callback_url)

    # Now, you have the credentials to send emails via Gmail API

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())