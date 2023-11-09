from dataclasses import dataclass

@dataclass
class GmailSession:
    gmail_service: object
    people_service: object 
    credentials: object

@dataclass
class OutlookSession:
    result: dict
    credentials: dict
