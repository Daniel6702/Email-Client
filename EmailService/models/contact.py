from dataclasses import dataclass

@dataclass
class Contact:
    name: str
    email: str
    resource_name: str = ''

    def display_text(self):
        return f"{self.name} <{self.email}>"
    
def generate_random_contact() -> Contact:
    return Contact(name="Test User", email="gmail@gmail.com")