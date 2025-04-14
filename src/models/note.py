from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Note(BaseModel):
    """
    Pydantic model for a note with title, content, tags, and timestamps.
    """

    id: Optional[int] = None
    title: str = Field(..., max_length=100, description="Title of the note")
    content: Optional[str] = Field(default=None, description="Content of the note")
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
