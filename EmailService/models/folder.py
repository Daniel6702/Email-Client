from dataclasses import dataclass, field
from typing import List

@dataclass
class Folder:
    name: str
    id: str
    children: List['Folder'] = field(default_factory=list)

    def __str__(self):
        return f"Name: {self.name}\nID: {self.id}\nChildren: {self.children}"

def print_folder_hierarchy(folders, indent=0):
    for folder in folders:
        print('  ' * indent + folder.name)
        print_folder_hierarchy(folder.children, indent + 1)