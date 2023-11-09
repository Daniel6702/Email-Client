from PyQt5.QtCore import QUrl, pyqtSlot,QFile, QIODevice
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import  QWebEnginePage
import os

#Custom WebEnginePage class to inject JavaScript into the page and allow for intercepting clicks on links and opening them in the default browser
#there is no direct access to the page elements the only way you can interact with the html/dom is via javascript -
#the web-page itself cannot tell you which element was clicked
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        js_file_path = os.path.join(current_dir, 'click_interceptor.js')
        try:
            with open(js_file_path, 'r') as js_file:
                js = js_file.read()
            self.add_objects({"jshelper": self})
            self.runJavaScript(js)
        except FileNotFoundError:
            print(f"The JavaScript file was not found at {js_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    @pyqtSlot(str)
    def openUrl(self, url):
        print(f"Request to open URL: {url}")
        QDesktopServices.openUrl(QUrl(url))