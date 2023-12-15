from PyQt5.QtWidgets import QLabel, QDesktopWidget, QVBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QListWidget, QListWidgetItem, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QIcon
import logging
from EmailService.models import Rule

class RulesLayout(QVBoxLayout):
    add_rule_signal = pyqtSignal(object)
    delete_rule_signal = pyqtSignal(object)

    def __init__(self, rules: list[Rule] = []):
        super().__init__()
        main_layout = QVBoxLayout()

        self.rules_list_widget = QListWidget()
        self.addWidgets(rules)

        self.add_rule_btn = QPushButton("Add Rule")
        self.add_rule_btn.clicked.connect(self.add_rule)

        self.delete_rule_btn = QPushButton("Delete Rule")
        self.delete_rule_btn.clicked.connect(self.delete_rule)

        main_layout.addWidget(self.rules_list_widget)
        main_layout.addWidget(self.add_rule_btn)
        main_layout.addWidget(self.delete_rule_btn)

        self.addLayout(main_layout)

    def addWidgets(self, rules: list[Rule]):
        for rule in rules:
            text = f"Name: {rule.name} \nConditions: {rule.conditions} \nActions: {rule.actions}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, rule) 
            self.rules_list_widget.addItem(item)

    def add_rule(self):
        dialog = QDialog()
        dialog.setWindowTitle("Add New Rule")
        dialog_layout = QFormLayout()

        name_line_edit = QLineEdit()
        conditions_line_edit = QLineEdit()
        actions_line_edit = QLineEdit()

        dialog_layout.addRow("Name:", name_line_edit)
        dialog_layout.addRow("Conditions (JSON):", conditions_line_edit)
        dialog_layout.addRow("Actions (JSON):", actions_line_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        dialog_layout.addWidget(buttons)
        dialog.setLayout(dialog_layout)

        if dialog.exec():
            name = name_line_edit.text()
            conditions = eval(conditions_line_edit.text())
            actions = eval(actions_line_edit.text())
            new_rule = Rule(
                name=name,
                conditions=conditions,
                actions=actions,
                id=None,
                sequence=1,
                is_enabled=True,
            )
            item = QListWidgetItem(f"Name: {new_rule.name} \nConditions: {new_rule.conditions} \nActions: {new_rule.actions}")
            item.setData(Qt.UserRole, new_rule)
            self.rules_list_widget.addItem(item)
            self.add_rule_signal.emit(new_rule)

    def delete_rule(self):
        selected_items = self.rules_list_widget.selectedItems()
        if selected_items:
            selected_rule = selected_items[0].data(Qt.UserRole)
            if selected_rule.id:
                self.delete_rule_signal.emit(selected_rule)
            self.rules_list_widget.takeItem(self.rules_list_widget.row(selected_items[0]))
        

class SettingsWindow(QWidget):
    add_rule_signal = pyqtSignal(object)
    delete_rule_signal = pyqtSignal(object)
    style_signal = pyqtSignal(str)
    switch_account_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initial_layout()
        main_layout = QGridLayout()

        # Left layout for buttons
        buttons_layout = QVBoxLayout()

        display_button = QPushButton("Display")
        rules_button = QPushButton("Rules")
        switch_account_button = QPushButton("Switch Account")
        logout_button = QPushButton("Log Out")

        display_button.clicked.connect(self.display_settings)
        rules_button.clicked.connect(self.rules_settings)
        switch_account_button.clicked.connect(self.switch_account_settings)
        logout_button.clicked.connect(self.logout_settings)

        buttons_layout.addWidget(display_button)
        buttons_layout.addWidget(rules_button)
        buttons_layout.addWidget(switch_account_button)
        buttons_layout.addWidget(logout_button)

        # Set the left layout for buttons
        #Set the stretch factor for the left layout columns
        main_layout.addLayout(buttons_layout, 0, 0, 2, 1) 
        main_layout.setColumnStretch(1, 3)

        # Right layout for content
        self.content_layout = QVBoxLayout()
        self.content_label = QLabel("Select an option on the left to view content.")

        # Set the right layout for content
        main_layout.addLayout(self.content_layout, 0, 1)
        self.setLayout(main_layout)

    def add_rules(self, rules: list[Rule]):
        self.rules = rules

    def initial_layout(self):
        self.setWindowTitle("Settings")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

    def display_settings(self):
        self.clear_content_layout()

        display_widget = QWidget()
        display_layout = QVBoxLayout()

        button1 = QPushButton("Light mode")
        button2 = QPushButton("Dark mode")
        button3 = QPushButton("Barbiemode")

        button1.clicked.connect(lambda: self.style_signal.emit("lightmode"))
        button2.clicked.connect(lambda: self.style_signal.emit("darkmode"))
        button3.clicked.connect(lambda: self.style_signal.emit("barbiemode"))

        display_layout.addWidget(button1)
        display_layout.addWidget(button2)
        display_layout.addWidget(button3)

        display_widget.setLayout(display_layout)
        self.content_layout.addWidget(display_widget)

    def rules_settings(self):
        self.clear_content_layout()
        self.rules_layout = RulesLayout(self.rules)
        self.rules_layout.add_rule_signal.connect(self.add_rule_signal.emit)
        self.rules_layout.delete_rule_signal.connect(self.delete_rule_signal.emit)
        temp = QWidget()
        temp.setLayout(self.rules_layout)
        self.content_layout.addWidget(temp)
        logging.info("Show Rules Settings")

    def switch_account_settings(self):
        self.clear_content_layout()
        display_widget = QWidget()
        display_layout = QVBoxLayout()
        self.content_label = QLabel("Are you sure you want to switch account?")
        self.content_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.content_label)
        button1 = QPushButton("Switch account")
        button1.clicked.connect(self.switch_account_signal.emit)
        display_layout.addWidget(button1)
        display_widget.setLayout(display_layout)
        self.content_layout.addWidget(display_widget)
        logging.info("Show Switch Account Settings")

    def logout_settings(self):
        self.clear_content_layout()
        display_widget = QWidget()
        display_layout = QVBoxLayout()
        self.content_label = QLabel("Are you sure you want to logout?")
        self.content_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.content_label)
        button1 = QPushButton("Logout")
        button1.clicked.connect(self.logout_signal.emit)
        display_layout.addWidget(button1)
        display_widget.setLayout(display_layout)
        self.content_layout.addWidget(display_widget)

    def clear_content_layout(self):
        if self.content_layout.count() > 0:
            items_to_remove = []

            for i in range(self.content_layout.count()):
                items_to_remove.append(self.content_layout.itemAt(i).widget())

            for item in items_to_remove:
                item.setParent(None)
