from dataclasses import dataclass
import json

@dataclass
class User:
    name: str
    email: str
    client_type: str
    credentials: dict

    def __str__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nClient Type: {self.client_type}\nCredentials: {self.credentials}"
    
    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        
        if type(data.get('credentials')) is str:
            return User(name=data.get('name'), email=data.get('email'), client_type=data.get('client_type'), credentials=json.loads(data.get('credentials')))
        
        return User(name=data.get('name'), email=data.get('email'), client_type=data.get('client_type'), credentials=data.get('credentials'))