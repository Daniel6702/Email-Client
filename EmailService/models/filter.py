from dataclasses import dataclass, fields
from datetime import datetime
from EmailService.models.folder import Folder
from typing import List, Optional

@dataclass
class Filter:
    before_date: Optional[datetime] = None
    after_date: Optional[datetime] = None
    from_email: Optional[str] = None
    to_email: Optional[str] = None
    is_read: Optional[bool] = None
    has_attachment: Optional[bool] = None
    contains: Optional[List[str]] = None
    not_contains: Optional[List[str]] = None
    folder: Optional[Folder] = None

    def is_empty(self) -> bool:
        return all(getattr(self, field.name) is None for field in fields(self))