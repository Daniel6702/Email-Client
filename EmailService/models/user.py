from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    client_type: str
    credentials: dict

    def __str__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nClient Type: {self.client_type}\nCredentials: {self.credentials}"

