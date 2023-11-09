from PyQt5.QtWidgets import QListWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt, QUrl, pyqtSlot,QFile, QIODevice
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import *
from email_util import Email
from PyQt5.QtWebChannel import QWebChannel

class EmailView(QVBoxLayout):
    def __init__(self, open_attachment_window: pyqtSignal(dict)):
        super().__init__()
        self.open_attachment_window = open_attachment_window
        self.current_email = None
        self.setupUIComponents()

    def on_console_message(self, message, line, source):
        print("Console message:", message)

    def setupUIComponents(self):
        #Email header
        self.from_user = QLineEdit()
        self.to_user = QLineEdit()
        self.subject = QLineEdit()
        self.from_user.setText("From: ")
        self.to_user.setText("To: ")
        self.subject.setText("Subject: ")

        #Email body
        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setHtml("<html><body><p>No email content to display. Select an email</p></body></html>")

        #Attachments list
        self.label = QLabel("attachments:")
        self.label.setVisible(False)
        self.label.setAlignment(Qt.AlignBottom)
        self.attachments_list = QListWidget()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.attachments_list.itemClicked.connect(self.onAttachmentClicked)

        #Layout
        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.from_user, 0, 0)
        grid_layout.addWidget(self.to_user, 1, 0)
        grid_layout.addWidget(self.subject, 2, 0)
        grid_layout.addWidget(self.browser, 3, 0)
        grid_layout.addWidget(self.label, 4, 0)
        grid_layout.addWidget(self.attachments_list, 5, 0)
        self.addLayout(grid_layout)

    def clearEmailView(self) -> None:
        self.from_user.setText("From: ")
        self.to_user.setText("To: ")
        self.subject.setText("Subject: ")
        self.browser.setHtml("<html><body><p>No email content to display. Select an email</p></body></html>")
        self.attachments_list.clear()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.label.setVisible(False)
      
    def updateEmailView(self, email: Email) -> None:
        self.clearEmailView()
        self.current_email = email
        self.from_user.setText(f"From: {email.from_email}")
        self.to_user.setText(f"To: {email.to_email}")
        self.subject.setText(f"Subject: {email.subject}")
        self.browser.setHtml(email.body)
        for attachment in email.attachments:
            self.label.setVisible(True)
            self.attachments_list.addItem(attachment['file_name'])
            self.attachments_list.setStyleSheet("QListWidget { border: 1px solid gray; }")
            item_height = 20
            total_height = item_height * self.attachments_list.count() + 4
            self.attachments_list.setFixedHeight(total_height)
            
    def onAttachmentClicked(self, item):
        for attachment in self.current_email.attachments:
            if attachment['file_name'] == item.text():
                self.previewAttachment(attachment)
                break
    
    def previewAttachment(self, attachment):
        self.open_attachment_window.emit(attachment)        
        #QMessageBox.information(QWidget(), "Attachment", f"You clicked {attachment['file_name']}")

#Custom WebEnginePage class to inject JavaScript into the page and allow for intercepting clicks on links and opening them in the default browser
#https://stackoverflow.com/questions/52197927/how-to-detect-button-click-inside-qwebengine-in-pyside2
class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)
        self.loadFinished.connect(self.onLoadFinished)
        print("WebEnginePage initialized")

    @pyqtSlot(bool)
    def onLoadFinished(self, ok):
        print("Finished loading:", ok)
        if ok:
            self.load_qwebchannel()
            self.run_scripts_on_load()
        else:
            print("Page did not load successfully")

    def load_qwebchannel(self):
        print("Loading qwebchannel.js...")
        file = QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            self.runJavaScript(content.data().decode())
            print("qwebchannel.js loaded")
        else:
            print("Failed to load qwebchannel.js")
        if self.webChannel() is None:
            channel = QWebChannel(self)
            self.setWebChannel(channel)
            print("QWebChannel set")

    def add_objects(self, objects):
        if self.webChannel() is not None:
            initial_script = ""
            end_script = ""
            self.webChannel().registerObjects(objects)
            print("Objects registered with the web channel")
            for name, obj in objects.items():
                initial_script += f"var {name};"
                end_script += f"{name} = channel.objects.{name};"
            js = initial_script + \
                 "new QWebChannel(qt.webChannelTransport, function (channel) {" + \
                 end_script + \
                 "} );"
            self.runJavaScript(js)
            print("Injected JavaScript to add objects to the web channel")

    def run_scripts_on_load(self):
        print("Injecting JavaScript for click interception...")
        js = '''
            document.addEventListener('click', function(event) {s
                var element = event.target;
                while (element != null && element.tagName != 'A') {
                    element = element.parentElement;
                }
                if (element != null && element.tagName === 'A') {
                    event.preventDefault();
                    jshelper.openUrl(element.href);
                }
            }, true);
        '''
        self.add_objects({"jshelper": self})
        self.runJavaScript(js)
    
    @pyqtSlot(str)
    def openUrl(self, url):
        print(f"Request to open URL: {url}")
        QDesktopServices.openUrl(QUrl(url))