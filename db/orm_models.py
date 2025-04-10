from sqlalchemy import Column, Integer, String, Date, Text, Index, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime



note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class NoteORM(Base):
    """
    SQLAlchemy ORM model for a note.
    """
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    modified_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    audit_message = Column(String, default="", nullable=False)
    # Many-to-many relationship with TagORM.
    tags = relationship("TagORM", secondary=note_tags, back_populates="notes")


class TagORM(Base):
    """
    SQLAlchemy ORM model for a tag.
    """
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    notes = relationship("NoteORM", secondary=note_tags, back_populates="tags")
    __table_args__ = (Index('ix_tags_name', "name"),)