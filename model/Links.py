from typing import Optional
from pydantic import BaseModel


class Links(BaseModel):
    self: str
    parent: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None