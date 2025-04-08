from typing import Optional, List

from pydantic import BaseModel, Field


class Note(BaseModel):
    """
    Pydantic model for a note with tags.
    """
    id: Optional[int] = None
    text: str = Field(..., max_length=1000)
    tags: List[str] = Field(default_factory=list)