from sqlalchemy import Column, Integer, String, Date, Text, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class PhoneBookRecordORM(Base):
    """
    SQLAlchemy ORM model for a phonebook record.
    """
    __tablename__ = "phonebook_records"
    __table_args__ = (Index("ix_phonebook_records_name", "name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=False)  # stored as string
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)


# Association table for the many-to-many relationship between notes and tags.
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
    __table_args__ = (Index("ix_notes_name", "name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    tags = relationship("TagORM", secondary=note_tags, back_populates="notes")


class TagORM(Base):
    """
    SQLAlchemy ORM model for a tag.
    """
    __tablename__ = 'tags'
    __table_args__ = (Index('ix_tags_name', "name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    notes = relationship("NoteORM", secondary=note_tags, back_populates="tags")