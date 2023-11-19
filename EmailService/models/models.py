from dataclasses import dataclass
from datetime import datetime
from EmailService.models.folder import Folder

@dataclass
class Filter:
    before_date: datetime = None
    after_date: datetime = None
    from_email: str = None
    to_email: str = None
    is_read: bool = None
    has_attachment: bool = None
    contains: list[str] = None
    not_contains: list[str] = None
    folder: Folder = Folder("","",[])