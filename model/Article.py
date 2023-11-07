from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    article_id: Optional[int] = None
    title: str
    slug: str
    content: str
    author: str