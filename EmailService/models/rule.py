import json
from dataclasses import dataclass

@dataclass
class Rule:
    name: str
    conditions: str 
    actions: str   
    id: str = None  
    sequence: int = None  
    is_enabled: bool = True  

    @property
    def conditions_json(self):
        try:
            return json.loads(self.conditions)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in conditions")

    @property
    def actions_json(self):
        try:
            return json.loads(self.actions)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in actions")



'''Conditions
{"sender": "example_sender@example.com"}
{"subjectContains": "example_subject"}
{"bodyContains": "example_body"}
'''

'''Actions
{"delete": True}
{"moveToFolder": "FolderName"}
{"setImportance": "High"}
'''

{"sender": "pedersendaniel356@gmail.com"}
{"setImportance": "High"}