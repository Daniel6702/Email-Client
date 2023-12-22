import sys
from PyQt5.QtWidgets import QApplication
from Controllers.app_controller import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_controller = AppController(app)
    sys.exit(app.exec_())

'''pyinstaller --noconfirm --onedir --windowed --icon "C:/Users/peder/Downloads/Icon_logo.ico" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/AI_SpamFilter;AI_SpamFilter/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/Certificates;Certificates/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/Controllers;Controllers/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/EmailService;EmailService/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/Images;Images/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/Testing;Testing/" --add-data "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/Views;Views/"  "C:/Users/peder/OneDrive - Aarhus universitet/Softwareteknologi/soeng_email_client/smail2.py"'''