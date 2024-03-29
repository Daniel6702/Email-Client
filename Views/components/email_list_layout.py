from PyQt5.QtWidgets import QAbstractItemView,QSizePolicy,QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal,Qt, QEvent, QSize,QTimer,QDateTime
from PyQt5.QtGui import *
from EmailService.models import Email
import html2text

class EmailWidget(QWidget):
    mark_email_as = pyqtSignal(Email, bool)
    delete_email = pyqtSignal(Email)

    def __init__(self, email: Email, parent=None):
        super().__init__(parent)
        self.email = email
        self.init_ui() 
        
    
    def init_ui(self):
        self.background_widget = QWidget(self)
        self.background_widget.setObjectName("background_widget")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)


        self.from_label = QLabel(f"From: {self.email.from_email[:50] if self.email.from_email else self.email.from_email}")
        self.from_label.setObjectName("from_label")
        self.subject_label = QLabel(f"Subject: {self.email.subject}")
        self.subject_label.setObjectName("subject_label")
        self.date_label = QLabel(f"Date: {self.email.datetime_info['date']}")
        self.date_label.setObjectName("subject_label")
        self.date_label.setAlignment(Qt.AlignRight)
        
        plain_text_body = html2text.html2text(self.email.body)
        # self.body_label = QLabel(f"Body: {plain_text_body[:50]}...")
        # self.body_label.setObjectName("body_label")
        
        # Use QLabel for the body
        self.body_label = QLabel()
        self.body_label.setObjectName("body_label")

        # Limit the number of visible lines in the QLabel
        max_visible_lines = 2
        lines = plain_text_body.split('\n')[:max_visible_lines]
        truncated_body = '\n'.join(lines)
        self.body_label.setText(f"Body: {truncated_body}...")
        
        
        self.read_button = QPushButton()
        self.read_button.setStatusTip("Mark as read")
        self.read_button.setObjectName("list_button")
        self.read_button.clicked.connect(self.on_mark_as)
        self.read_button.setMaximumWidth(30)

        self.delete_button = QPushButton()
        self.delete_button.setStatusTip("Delete email")
        self.delete_button.setIcon(QIcon("Images\\trash.png"))
        self.delete_button.setObjectName("list_button")
        self.delete_button.clicked.connect(self.on_delete_email)
        self.delete_button.setMaximumWidth(30)

        top_row = QHBoxLayout()
        top_row.addWidget(self.from_label)
        top_row.addWidget(self.read_button)
        top_row.addWidget(self.delete_button)
        
        mid_row = QHBoxLayout()
        mid_row.addWidget(self.subject_label)
        mid_row.addWidget(self.date_label,0, Qt.AlignRight)

        layout.addLayout(top_row)
        layout.addLayout(mid_row)
        layout.addWidget(self.body_label)

        #create checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("list_checkbox")
        self.checkbox.setMaximumWidth(25)
        self.checkbox.stateChanged.connect(lambda state: self.checkbox_changed_callback(state))


        temp = QHBoxLayout()
        temp.addWidget(self.checkbox)
        temp.addLayout(layout)

        self.background_widget.setLayout(temp)        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.background_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setLayout(main_layout)

        self.background_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def checkbox_changed_callback(self, state):
        # Handle checkbox state change here
        pass

    
    def mark_email_as_read(self,new_background=None):
        self.read_button.setIcon(QIcon("Images\\mark_unread.png"))
        self.email.is_read = True
        if not new_background:
            new_background = self.from_label.palette().color(QPalette.Background)
        self.background_widget.setStyleSheet("background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.from_label.setStyleSheet("font-weight: normal; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.subject_label.setStyleSheet("font-weight: normal; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.date_label.setStyleSheet("font-weight: normal; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.body_label.setStyleSheet("font-weight: normal; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))

    def mark_email_as_unread(self,new_background=None):
        self.read_button.setIcon(QIcon("Images\\mark_read.png"))
        self.email.is_read = False
        if not new_background:
            new_background = self.from_label.palette().color(QPalette.Background)
        self.background_widget.setStyleSheet("background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.from_label.setStyleSheet("font-weight: bold; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.subject_label.setStyleSheet("font-weight: bold; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.date_label.setStyleSheet("font-weight: bold; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
        self.body_label.setStyleSheet("font-weight: bold; background-color: rgb({},{},{});".format(new_background.red(), new_background.green(), new_background.blue()))
    
    def on_mark_as(self):
        if self.email.is_read:
            self.mark_email_as.emit(self.email, False)
        else:
            self.mark_email_as.emit(self.email, True)
        
    def on_delete_email(self):
        self.delete_email.emit(self.email)

class EmailListArea(QVBoxLayout):
    email_clicked = pyqtSignal(Email)
    mark_email_as = pyqtSignal(Email, bool)
    email_deleted = pyqtSignal(Email)
    new_page = pyqtSignal(int)
    refresh_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_page = 1
        self.selected_emails = []
        self.last_selected_email = None

        self.setup_email_list()

        update_interval_seconds = 90
        self.start_periodic_updates(update_interval_seconds)

    def setup_email_list(self):
        label = QLabel("Emails:")
        refresh = QPushButton(QIcon("Images\\refresh.png"),"")
        refresh.setStatusTip("Refresh")
        refresh.setObjectName("refresh_button")
        refresh.clicked.connect(self.refresh_signal.emit)
        
        #New Buttons
        self.delete_selected_button = QPushButton("Delete")
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.delete_selected_button.setVisible(False)  # Initially hidden
        self.mark_as_read_button = QPushButton("Mark as Read")
        self.mark_as_read_button.clicked.connect(self.mark_selected_as_read)
        self.mark_as_read_button.setVisible(False)  # Initially hidden
        self.mark_as_unread_button = QPushButton("Mark as Unread")
        self.mark_as_unread_button.clicked.connect(self.mark_selected_as_unread)
        self.mark_as_unread_button.setVisible(False)  
        
        temp = QHBoxLayout()
        temp.addWidget(label)
        temp.addWidget(self.delete_selected_button)
        temp.addWidget(self.mark_as_read_button)
        temp.addWidget(self.mark_as_unread_button)
        temp.addWidget(refresh)
        self.addLayout(temp)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("email_list")
        self.list_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timer_timeout)
        self.currently_clicked_item = None

        # Connect the list widget's item selection signal
        self.list_widget.itemSelectionChanged.connect(self.handle_item_selection_changed)

        bottom_layout = QHBoxLayout()

        self.previous_page_button = QPushButton("Previous Page")
        self.previous_page_button.setMaximumWidth(120)
        self.previous_page_button.clicked.connect(self.previous_page)
        bottom_layout.addWidget(self.previous_page_button)

        self.page_number_label = QLabel(f"Page {self.current_page}")
        bottom_layout.addWidget(self.page_number_label)

        self.next_page_button = QPushButton("Next Page")
        self.next_page_button.setMaximumWidth(120)
        self.next_page_button.clicked.connect(self.next_page)
        bottom_layout.addWidget(self.next_page_button)

        self.addLayout(bottom_layout)

    def checkbox_changed_callback(self, email_widget, state):
        if email_widget.email in self.selected_emails and not state:
            self.selected_emails.remove(email_widget.email)
        elif state:
            self.selected_emails.append(email_widget.email)

        self.update_button_visibility()

    def update_button_visibility(self):
        has_selection = len(self.selected_emails) > 0
        self.delete_selected_button.setVisible(has_selection)
        self.mark_as_read_button.setVisible(has_selection)
        self.mark_as_unread_button.setVisible(has_selection)
            
    def delete_selected(self):
        for email in self.selected_emails:
            self.delete_email(email)
        # self.selected_emails = []
        self.clear_selected_checkboxes()

    def mark_selected_as_read(self):
        for email in self.selected_emails:
            if not email.is_read:
                self.mark_email_as.emit(email, True)
        # self.selected_emails = []
        self.clear_selected_checkboxes()

    def mark_selected_as_unread(self):
        for email in self.selected_emails:
            if email.is_read:
                self.mark_email_as.emit(email, False)
        # self.selected_emails = []
        self.clear_selected_checkboxes()
        
    def clear_selected_checkboxes(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            email_widget = self.list_widget.itemWidget(item)
            if email_widget:
                email_widget.checkbox.setChecked(False)

        self.selected_emails = []
    
    def next_page(self):
        self.current_page += 1
        self.page_number_label.setText(f"Page {self.current_page}")
        self.new_page.emit(self.current_page)

    def previous_page(self): 
        if self.current_page > 1:
            self.current_page -= 1
            self.page_number_label.setText(f"Page {self.current_page}")
            self.new_page.emit(self.current_page)

    def add_emails_to_list(self, mails: list[Email]):
        self.list_widget.clear()
        self.selected_emails = []
        for mail in mails:
            self.add_email_to_list(mail)
        for mail in mails:
            self.mark_as_func(mail, mail.is_read)
        
    def add_email_to_list(self, mail: Email):
        email_widget = EmailWidget(mail)
        email_widget.mark_email_as.connect(self.mark_email_as)
        email_widget.delete_email.connect(self.delete_email)
        email_widget.setMaximumWidth(self.list_widget.width()+10)

        # Connect the stateChanged signal of the checkbox to the checkbox_changed_callback method
        email_widget.checkbox.stateChanged.connect(lambda state, widget=email_widget: self.checkbox_changed_callback(widget, state))

        item = QListWidgetItem()
        item.setSizeHint(email_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, email_widget)        

    def mark_as_func(self, mail: Email, is_read: bool):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            email_widget = self.list_widget.itemWidget(item)
            if email_widget and email_widget.email == mail:
                if is_read:
                    new_color = QColor(250,250,250)
                    email_widget.mark_email_as_read(new_color)
                else:
                    new_color = QColor(220,220,220)
                    email_widget.mark_email_as_unread(new_color)
                break

    def update_email_in_list(self, mail: Email):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            email_widget = self.list_widget.itemWidget(item)
            if email_widget and email_widget.email == mail:
                email_widget.email = mail
                email_widget.from_label.setText(f"From: {mail.from_email}")
                email_widget.subject_label.setText(f"Subject: {mail.subject}")
                email_widget.date_label.setText(f"Date: {mail.datetime_info['date']}")
                email_widget.body_label.setText(f"Body: {mail.body[:50]}...")
                self.mark_as_func(mail, mail.is_read)
                break

    def handle_item_clicked(self, item: QListWidgetItem):
        widget = self.list_widget.itemWidget(item)
        if hasattr(widget, 'email'):
            if self.last_selected_email == widget.email:
                # If the same email is clicked again, emit the signal with an empty email and reset the last selected email
                self.list_widget.clearSelection()
                self.email_clicked.emit(Email(None, None, None, None, None, None, None, None))
                self.last_selected_email = None
            else:
                # If a different email is clicked, emit the signal with the selected email
                self.email_clicked.emit(widget.email)
                self.last_selected_email = widget.email
            self.currently_clicked_item = item

        if not widget.email.is_read:
            self.timer.start(2000)
    
    def handle_item_selection_changed(self):
        # This method is called when the item selection changes
        if self.timer.isActive():
            self.timer.stop()

    def handle_timer_timeout(self):
        # This method is called when the timer times out
        if self.currently_clicked_item is not None:
            widget = self.list_widget.itemWidget(self.currently_clicked_item)
            if widget and hasattr(widget, 'email'):
                self.mark_email_as.emit(widget.email, True)
                self.timer.stop()
                self.currently_clicked_item = None
           
    # def mark_email_as_read(self, email):
    #     self.mark_email_as.emit(email, True)
    #     self.timer.stop()
    

    def delete_email(self, mail: Email):
        reply = QMessageBox.question(None, 'Delete email', 
                                     "Are you sure you want to delete this email?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.email_deleted.emit(mail)
            self.remove_email_from_list(mail)
            

    def remove_email_from_list(self, mail: Email):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            email_widget = self.list_widget.itemWidget(item)
            if email_widget and email_widget.email == mail:
                self.list_widget.takeItem(index)
                break

    def start_periodic_updates(self, interval_seconds):
        self.timer_updates = QTimer(self)
        self.timer_updates.timeout.connect(self.handle_periodic_update)
        self.timer_updates.start(interval_seconds * 1000)

    def handle_periodic_update(self):
        self.refresh_signal.emit()