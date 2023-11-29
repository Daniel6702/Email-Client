from dataclasses import dataclass

@dataclass
class Rule:
    name: str
    conditions: dict 
    actions: dict   
    id: str = None

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