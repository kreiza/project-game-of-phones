from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import func

from db.database import SessionLocal
from db.orm_models import ContactORM
from src.common.repository import AbstractRepository
from src.models.record import Contact


class ContactRepository(AbstractRepository[Contact]):
    """
    Concrete repository implementation using SQLite and SQLAlchemy.
    Handles CRUD operations for Contact records and includes
    search-by-name and search-by-birthday functionalities.
    """

    def add(self, record: Contact) -> Contact:
        """
        Add a new phonebook record to the SQLite database.
        """
        with SessionLocal() as session:
            orm_record = ContactORM(
                name=record.name,
                phone_number=str(record.phone_number),
                address=record.address,
                email=record.email,
                birthday=record.birthday,
                contact_note=record.contact_note,
            )
            session.add(orm_record)
            session.commit()
            session.refresh(orm_record)
            return Contact(
                id=orm_record.id,
                name=orm_record.name,
                phone_number=orm_record.phone_number,
                address=orm_record.address,
                email=orm_record.email,
                birthday=orm_record.birthday,
                contact_note=orm_record.contact_note,
            )

    def get_by_id(self, record_id: int) -> Optional[Contact]:
        """
        Retrieve a phonebook record by its ID.
        """
        with SessionLocal() as session:
            orm_record = session.get(ContactORM, record_id)
            if orm_record:
                return Contact(
                    id=orm_record.id,
                    name=orm_record.name,
                    phone_number=orm_record.phone_number,
                    address=orm_record.address,
                    email=orm_record.email,
                    birthday=orm_record.birthday,
                    contact_note=orm_record.contact_note,
                )
            return None

    def list_all(self) -> List[Contact]:
        """
        List all phonebook records.
        """
        with SessionLocal() as session:
            orm_records = session.query(ContactORM).all()
            return [
                Contact(
                    id=rec.id,
                    name=rec.name,
                    phone_number=rec.phone_number,
                    address=rec.address,
                    email=rec.email,
                    birthday=rec.birthday,
                    contact_note=rec.contact_note,
                )
                for rec in orm_records
            ]

    def update(self, record_id: int, updates: Dict[str, Any]) -> Optional[Contact]:
        """
        Update a phonebook record with the given updates.

        :param record_id: The ID of the record to update.
        :param updates: A dictionary of fields to update.
        :return: The updated Contact if successful, otherwise None.
        """
        with SessionLocal() as session:
            orm_record = session.get(ContactORM, record_id)
            if not orm_record:
                return None

            for key, value in updates.items():
                # Update only if the attribute exists and the provided value is not None.
                if hasattr(orm_record, key) and value is not None:
                    setattr(orm_record, key, value)
            session.commit()
            session.refresh(orm_record)
            return Contact(
                id=orm_record.id,
                name=orm_record.name,
                phone_number=orm_record.phone_number,
                address=orm_record.address,
                email=orm_record.email,
                birthday=orm_record.birthday,
                contact_note=orm_record.contact_note,
            )

    def delete(self, record_id: int) -> bool:
        """
        Delete a phonebook record by its ID.

        :param record_id: The ID of the record to delete.
        :return: True if deletion was successful, False otherwise.
        """
        with SessionLocal() as session:
            orm_record = session.get(ContactORM, record_id)
            if not orm_record:
                return False
            session.delete(orm_record)
            session.commit()
            return True

    def search_by_name(self, name: str) -> List[Contact]:
        """
        Search for phonebook records that contain the given name substring (case-insensitive).

        :param name: The substring to search for in names.
        :return: A list of Contact instances that match the search.
        """
        with SessionLocal() as session:
            orm_records = (
                session.query(ContactORM)
                .filter(ContactORM.name.ilike(f"%{name}%"))
                .all()
            )
            return [
                Contact(
                    id=rec.id,
                    name=rec.name,
                    phone_number=rec.phone_number,
                    address=rec.address,
                    email=rec.email,
                    birthday=rec.birthday,
                    contact_note=rec.contact_note,
                )
                for rec in orm_records
            ]

    def search_by_birthday_after(self, days: int) -> List[Contact]:
        """
        Search for contacts with birthdays that fall on the day 'days' from today.
        This method compares only the month and day of the birthday.

        :param days: The number of days from today.
        :return: A list of Contact instances with birthdays on the target day.
        """
        target_date = date.today() + timedelta(days=days)
        target_str = target_date.strftime("%m-%d")
        with SessionLocal() as session:
            orm_records = (
                session.query(ContactORM)
                .filter(func.strftime("%m-%d", ContactORM.birthday) == target_str)
                .all()
            )
            return [
                Contact(
                    id=rec.id,
                    name=rec.name,
                    phone_number=rec.phone_number,
                    address=rec.address,
                    email=rec.email,
                    birthday=rec.birthday,
                    contact_note=rec.contact_note,
                )
                for rec in orm_records
            ]
