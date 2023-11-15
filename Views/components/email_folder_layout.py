from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QWidget, QListWidgetItem
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

    def __init__(self):
        super().__init__()
        self.setup_folder_field_layout()
        self.folder_widgets = {} 
        self.folder_items = {}

    def setup_folder_field_layout(self):
        label = QLabel("Folders:")
        self.addWidget(label)
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
            self.folder_selected.emit(widget.folder)

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