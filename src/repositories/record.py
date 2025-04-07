from typing import List, Optional, Dict, Any

from src.common.repository import AbstractRepository
from src.common.models import PhoneBookRecord
from db.database import SessionLocal
from db.orm_models import PhoneBookRecordORM



class PhoneBookRecordRepository(AbstractRepository):
    """
    Concrete repository implementation using SQLite and SQLAlchemy.
    """

    def add(self, record: PhoneBookRecord) -> PhoneBookRecord:
        """
        Add a new phonebook record to the SQLite database.
        """
        with SessionLocal() as session:
            orm_record = PhoneBookRecordORM(
                name=record.name,
                phone_number=str(record.phone_number),
                address=record.address,
                email=record.email,
                birthday=record.birthday,
                notes=record.notes,
            )
            session.add(orm_record)
            session.commit()
            session.refresh(orm_record)
            return PhoneBookRecord(
                id=orm_record.id,
                name=orm_record.name,
                phone_number=orm_record.phone_number,
                address=orm_record.address,
                email=orm_record.email,
                birthday=orm_record.birthday,
                notes=orm_record.notes,
            )

    def get_by_id(self, record_id: int) -> Optional[PhoneBookRecord]:
        """
        Retrieve a phonebook record by its ID.
        """
        with SessionLocal() as session:
            orm_record = session.get(PhoneBookRecordORM, record_id)
            if orm_record:
                return PhoneBookRecord(
                    id=orm_record.id,
                    name=orm_record.name,
                    phone_number=orm_record.phone_number,
                    address=orm_record.address,
                    email=orm_record.email,
                    birthday=orm_record.birthday,
                    notes=orm_record.notes,
                )
            return None

    def list_all(self) -> List[PhoneBookRecord]:
        """
        List all phonebook records.
        """
        with SessionLocal() as session:
            orm_records = session.query(PhoneBookRecordORM).all()
            return [
                PhoneBookRecord(
                    id=rec.id,
                    name=rec.name,
                    phone_number=rec.phone_number,
                    address=rec.address,
                    email=rec.email,
                    birthday=rec.birthday,
                    notes=rec.notes,
                )
                for rec in orm_records
            ]

    def update(self, record_id: int, updates: Dict[str, Any]) -> Optional[PhoneBookRecord]:
        """
        Update a phonebook record with the given updates.

        :param record_id: The ID of the record to update.
        :param updates: A dictionary of fields to update.
        :return: The updated PhoneBookRecord if successful, otherwise None.
        """
        with SessionLocal() as session:
            orm_record = session.get(PhoneBookRecordORM, record_id)
            if not orm_record:
                return None

            for key, value in updates.items():
                if hasattr(orm_record, key) and value is not None:
                    setattr(orm_record, key, value)
            session.commit()
            session.refresh(orm_record)
            return PhoneBookRecord(
                id=orm_record.id,
                name=orm_record.name,
                phone_number=orm_record.phone_number,
                address=orm_record.address,
                email=orm_record.email,
                birthday=orm_record.birthday,
                notes=orm_record.notes,
            )

    def delete(self, record_id: int) -> bool:
        """
        Delete a phonebook record by its ID.

        :param record_id: The ID of the record to delete.
        :return: True if deletion was successful, False otherwise.
        """
        with SessionLocal() as session:
            orm_record = session.get(PhoneBookRecordORM, record_id)
            if not orm_record:
                return False
            session.delete(orm_record)
            session.commit()
            return True
