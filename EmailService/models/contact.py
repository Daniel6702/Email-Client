from dataclasses import dataclass

@dataclass
class Contact:
    name: str
    email: str
    resource_name: str = ''