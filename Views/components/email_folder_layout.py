from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QWidget, QListWidgetItem, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QPixmap
from EmailService.models import Folder
from typing import List

class FolderWidget(QWidget):
    def __init__(self, folder: Folder, indent_level: int, parent=None):
        super().__init__(parent)
        self.folder = folder
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0) 

        indent_width = indent_level * 20 
        if indent_width > 0:
            self.layout.addSpacerItem(QSpacerItem(indent_width, 10, QSizePolicy.Fixed))

        if folder.children:
            self.button = QPushButton('v')
            self.button.setCheckable(True)
            self.button.setChecked(False)
            self.button.setObjectName('folder_button')
            self.button.setMaximumWidth(20)
            self.button.clicked.connect(self.on_button_clicked)
            self.layout.addWidget(self.button)
        else:
            indent_label = QLabel(' ')
            indent_label.setObjectName('folder_label')
            indent_label.setMaximumWidth(20)
            self.layout.addWidget(indent_label)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("Images\\folder_icon.png"))
        icon_label.setScaledContents(True)
        icon_label.setMaximumSize(50, 50)
        self.layout.addWidget(icon_label)

        self.label = QLabel(folder.name)
        self.label.setObjectName('folder_label')
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter)

    def on_button_clicked(self):
        if self.button.isChecked():
            self.button.setText('>')
        else:
            self.button.setText('v')
        self.toggle_children.emit(self.folder)

    toggle_children = pyqtSignal(object)

class FolderArea(QVBoxLayout):
    folder_selected = pyqtSignal(object) 
    delete_folder_signal = pyqtSignal(object)
    edit_folder_signal = pyqtSignal(object, str)
    add_folder_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_buttons()
        self.setup_folder_field_layout()
        self.folder_widgets = {} 
        self.folder_items = {}

    def setup_buttons(self):
        label = QLabel("Folders:")
        self.addWidget(label)
        self.button_layout = QHBoxLayout()

        self.add_folder_button = QPushButton('Add')
        self.add_folder_button.clicked.connect(self.add_folder_button_clicked)
        self.delete_folder_button = QPushButton('Delete')
        self.delete_folder_button.setCheckable(True)
        self.delete_folder_button.clicked.connect(self.checkable_buttons_clicked)
        self.edit_folder_button = QPushButton('Edit')
        self.edit_folder_button.setCheckable(True)
        self.edit_folder_button.clicked.connect(self.checkable_buttons_clicked)

        self.button_layout.addWidget(self.add_folder_button)
        self.button_layout.addWidget(self.delete_folder_button)
        self.button_layout.addWidget(self.edit_folder_button)

        self.addLayout(self.button_layout)
    
    def checkable_buttons_clicked(self):
        if self.delete_folder_button.isChecked() or self.edit_folder_button.isChecked():
            QMessageBox.information(self.parent, "Select a Folder", "Please select a folder.", QMessageBox.Ok)
    
    def add_folder_button_clicked(self):
        text, okPressed = QInputDialog.getText(self.parent, "Add New Folder", "Enter folder name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            folder = Folder(name=text, id=None, children=[])
            self.add_folder_signal.emit(folder)
            self.refresh_folder_list()

    def delete_folder(self, folder: Folder):
        reply = QMessageBox.question(self.parent, 'Delete folder', 
                                     "Are you sure you want to delete this folder?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_folder_signal.emit(folder)
            self.remove_folder(folder)
        self.delete_folder_button.setChecked(False)

    def edit_folder(self, folder: Folder):
        text, okPressed = QInputDialog.getText(self.parent, "Edit folder name", "Enter new folder name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.edit_folder_signal.emit(folder, text)
            self.refresh_folder_list()
        self.edit_folder_button.setChecked(False)

    def setup_folder_field_layout(self):
        self.list_widget = QListWidget()
        self.list_widget.setObjectName('folder_list')
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def move_inbox_to_top(self, folders: List['Folder']) -> List['Folder']:
        for index, folder in enumerate(folders):
            if folder.name in ['Inbox', 'inbox', 'INBOX']:
                folders.insert(0, folders.pop(index))
                self.folder_selected.emit(folder)  # Initialize the email list with the inbox
                break
        return folders
    
    def add_folders(self, folders: List['Folder']):
        self.folders = folders
        folders = self.move_inbox_to_top(folders)
        for folder in folders:
            self.add_folder(folder, 0)
        self.list_widget.setCurrentItem(self.list_widget.item(0))

    def add_folder(self, folder: 'Folder', indent_level):
        item = QListWidgetItem()
        custom_widget = FolderWidget(folder, indent_level)
        custom_widget.toggle_children.connect(self.hide_show_subfolders)
        item.setSizeHint(custom_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, custom_widget)
        item.setData(Qt.UserRole, folder)

        self.folder_widgets[folder.id] = custom_widget
        self.folder_items[folder.id] = item 

        for child in folder.children:
            self.add_folder(child, indent_level + 1)

    def hide_show_subfolders(self, folder):
        visible = not self.folder_widgets[folder.id].button.isChecked()
        self._set_children_visibility(folder, visible)

    def _set_children_visibility(self, folder, visible):
        for child in folder.children:
            child_widget = self.folder_widgets[child.id]
            child_item = self.folder_items[child.id]

            child_widget.setVisible(visible)
            child_item.setHidden(not visible)

            if child.children and not visible:
                self._set_children_visibility(child, visible)

    def handle_item_clicked(self, item):
        widget = self.list_widget.itemWidget(item)
        if hasattr(widget, 'folder'):
            folder = widget.folder
        else:
            return
        if self.delete_folder_button.isChecked():
            self.delete_folder(folder)
        elif self.edit_folder_button.isChecked():
            self.edit_folder(folder)
        else:
            self.folder_selected.emit(folder)

    def remove_folder(self, folder: 'Folder'):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.data(Qt.UserRole).id == folder.id:
                self.list_widget.takeItem(index)
                self._remove_folder_and_children_from_dicts(folder)
                break

    def _remove_folder_and_children_from_dicts(self, folder):
        del self.folder_widgets[folder.id]
        del self.folder_items[folder.id]
        for child in folder.children:
            self._remove_folder_and_children_from_dicts(child)

    def clear_folders(self):
        self.list_widget.clear()
        self.folder_widgets.clear()
        self.folder_items.clear()

    def select_folder_by_id(self, folder_id: str):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.data(Qt.UserRole).id == folder_id:
                self.list_widget.setCurrentItem(item)
                break

    def refresh_folder_list(self):
        self.clear_folders()
        self.add_folders(self.folders)