from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    comment_id: Optional[int] = None
    title : str
    content: str
    # article_id: int