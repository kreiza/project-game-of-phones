from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from db.database import Base


class ContactORM(Base):
    """
    SQLAlchemy ORM model for a phonebook record.
    """

    __tablename__ = "contacts"
    __table_args__ = (
        Index("ix_contacts_name", "name"),
        Index("ix_contacts_birthday", "birthday"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=False)  # stored as string
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    contact_note = Column(Text, nullable=True)  # renamed from "notes"


# Association table for the many-to-many relationship between notes and tags.
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class NoteORM(Base):
    """
    SQLAlchemy ORM model for a note.
    """

    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)  # Changed to Text to allow longer content
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    modified_at = Column(
        DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )
    # Many-to-many relationship with TagORM.
    tags = relationship("TagORM", secondary=note_tags, back_populates="notes")


class TagORM(Base):
    """
    SQLAlchemy ORM model for a tag.
    """

    __tablename__ = "tags"
    __table_args__ = (Index("ix_tags_name", "name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    notes = relationship("NoteORM", secondary=note_tags, back_populates="tags")
