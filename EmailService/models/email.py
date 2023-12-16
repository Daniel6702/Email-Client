from dataclasses import dataclass, field
from typing import List
import html
from datetime import datetime
from EmailService.models.folder import Folder

@dataclass
class Email:
    from_email: str
    to_email: list[str]
    subject: str
    body: str
    datetime_info: dict
    attachments: List[dict] = field(default_factory=list)
    id: str = None
    is_read: bool = False
    folder: Folder = None
    bcc: list[str] = field(default_factory=list)
    cc: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        if self.from_email == None or self.from_email == "" \
        or self.to_email == None or self.to_email == [] \
        or self.subject == None or self.subject == "" \
        or self.body == None or self.body == "" \
        or self.datetime_info == None or self.datetime_info == {}:
            return True
        else:
            return False

    def __str__(self, body_limit: int = 500):
        email_info = [
            "=====================================",
            "\nEmail Info:\n",
            f"Email ID: {self.id or 'N/A'}",
            f"From: {self.from_email}",
            f"To: {self.to_email}",
            f"Subject: {self.subject}",
            f"Date and Time: {self.datetime_info}",
            f"Is Read: {'Yes' if self.is_read else 'No'}",
            "Attachments:"
        ]
        for attachment in self.attachments:
            email_info.append(f"  - {attachment['file_name']}")
        
        email_info.append("\nEmail Body:\n")
        truncated_body = (self.body[:body_limit] + '...') if len(self.body) > body_limit else self.body
        email_info.append(truncated_body)

        return '\n'.join(email_info)

def generate_test_email() -> Email:
    return Email(   from_email="dacasoftdev.test@gmail.com",
                    to_email=["dacasoftdev_test@hotmail.com"],
                    subject="Test Email",
                    body=f"""
                        <!DOCTYPE html>
                        <html>
                        <body>
                            <p>{html.escape("This is a test Email")}</p>
                        </body>
                        </html>
                        """,
                    datetime_info = {'date': str(datetime.now().date()),
                                    'time': str(datetime.now().time())},
                    attachments=[],
                    id=None,
                    is_read=False)
