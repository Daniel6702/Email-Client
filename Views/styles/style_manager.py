import os
import re    
import json


class StyleManager():
    def __init__(self, app):
        self.app = app
        self.set_style('lightmode')

    def set_style(self, style):
        self.current_style = style
        self.color_dict = self.get_color_dict(style)
        self.load_stylesheets()

    def get_color_dict(self, style, path: str = "Views\\styles\\color_dict.json") -> dict:
        with open(path, "r") as f:
            color_dict = json.load(f)
        return color_dict[style]

    def get_stylesheet(self, folder_path: str = "Views\\styles\\") -> str:
        combined_style = ""
        for filename in os.listdir(folder_path):
            if filename.endswith(".qss"):
                with open(os.path.join(folder_path, filename), "r") as f:
                    combined_style += f.read() + "\n"

        for key, color in self.color_dict.items():
            combined_style = re.sub(f"%{key}%", color, combined_style)
        return combined_style

    def load_stylesheets(self):
        style_sheet = self.get_stylesheet()
        self.app.setStyleSheet(style_sheet)