from sqlalchemy import Column, Integer, String, Date, Text, Index
from db.database import Base

class PhoneBookRecordORM(Base):
    """
    SQLAlchemy ORM model for a phonebook record.
    """
    __tablename__ = "phonebook_records"
    __table_args__ = (
        Index('ix_phonebook_records_name', 'name'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=False)  # stored as string
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
