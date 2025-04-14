from datetime import datetime
from typing import Any, Dict, List, Optional

from db.database import SessionLocal
from db.orm_models import NoteORM, TagORM
from src.common.repository import AbstractRepository
from src.models.note import Note


class NoteRepository(AbstractRepository[Note]):
    """
    Concrete repository implementation for notes using SQLite and SQLAlchemy.
    Implements the generic repository interface for the Note model.
    """

    def add(self, note: Note) -> Note:
        """
        Add a new note, along with its content and tags, to the repository.
        :param note: The Note instance to add.
        :return: The added Note instance with an assigned ID.
        """
        with SessionLocal() as session:
            tag_objs = []
            # Find or create tag objects based on the given tag names.
            for tag in note.tags:
                tag_obj = session.query(TagORM).filter(TagORM.name == tag).first()
                if not tag_obj:
                    tag_obj = TagORM(name=tag)
                    session.add(tag_obj)
                tag_objs.append(tag_obj)

            orm_note = NoteORM(
                title=note.title,
                content=note.content,
                created_at=note.created_at,
                modified_at=note.modified_at,
                tags=tag_objs,
            )
            session.add(orm_note)
            session.commit()
            session.refresh(orm_note)
            return Note(
                id=orm_note.id,
                title=orm_note.title,
                content=orm_note.content,
                created_at=orm_note.created_at,
                modified_at=orm_note.modified_at,
                tags=[t.name for t in orm_note.tags],
            )

    def get_by_id(self, note_id: int) -> Optional[Note]:
        """
        Retrieve a note by its ID.
        :param note_id: The unique identifier of the note.
        :return: The Note instance if found, otherwise None.
        """
        with SessionLocal() as session:
            orm_note = session.get(NoteORM, note_id)
            if orm_note:
                return Note(
                    id=orm_note.id,
                    title=orm_note.title,
                    content=orm_note.content,
                    created_at=orm_note.created_at,
                    modified_at=orm_note.modified_at,
                    tags=[t.name for t in orm_note.tags],
                )
            return None

    def list_all(self) -> List[Note]:
        """
        List all notes in the repository.
        :return: A list of Note instances.
        """
        with SessionLocal() as session:
            orm_notes = session.query(NoteORM).all()
            return [
                Note(
                    id=n.id,
                    title=n.title,
                    content=n.content,
                    created_at=n.created_at,
                    modified_at=n.modified_at,
                    tags=[t.name for t in n.tags],
                )
                for n in orm_notes
            ]

    def update(self, note_id: int, updates: Dict[str, Any]) -> Optional[Note]:
        """
        Update an existing note with the provided fields.
        The updates dictionary can contain:
          - "title": new note title
          - "content": new note content
          - "tags": new list of tag names
        :param note_id: The unique identifier of the note to update.
        :param updates: A dictionary of fields to update.
        :return: The updated Note if successful, otherwise None.
        """
        with SessionLocal() as session:
            orm_note = session.get(NoteORM, note_id)
            if not orm_note:
                return None

            if "title" in updates and updates["title"] is not None:
                orm_note.title = updates["title"]

            if "content" in updates and updates["content"] is not None:
                orm_note.content = updates["content"]

            if "tags" in updates and updates["tags"] is not None:
                new_tags = []
                for tag in updates["tags"]:
                    tag_obj = session.query(TagORM).filter(TagORM.name == tag).first()
                    if not tag_obj:
                        tag_obj = TagORM(name=tag)
                        session.add(tag_obj)
                    new_tags.append(tag_obj)
                orm_note.tags = new_tags

            orm_note.modified_at = datetime.now()
            session.commit()
            session.refresh(orm_note)

            return Note(
                id=orm_note.id,
                title=orm_note.title,
                content=orm_note.content,
                tags=[t.name for t in orm_note.tags],
                created_at=orm_note.created_at,
                modified_at=orm_note.modified_at,
            )

    def delete(self, note_id: int) -> bool:
        """
        Delete a note by its ID.
        :param note_id: The unique identifier of the note to delete.
        :return: True if deletion was successful, otherwise False.
        """
        with SessionLocal() as session:
            orm_note = session.get(NoteORM, note_id)
            if not orm_note:
                return False
            session.delete(orm_note)
            session.commit()
            return True

    def search_by_title(self, keyword: str) -> List[Note]:
        """
        Search for notes that contain the specified title substring (case-insensitive).
        :param keyword: The substring to search in note titles.
        :return: A list of Note instances that match the title.
        """
        with SessionLocal() as session:
            orm_notes = (
                session.query(NoteORM).filter(NoteORM.title.ilike(f"%{keyword}%")).all()
            )

            return [
                Note(
                    id=n.id,
                    title=n.title,
                    content=n.content,
                    created_at=n.created_at,
                    modified_at=n.modified_at,
                    tags=[t.name for t in n.tags],
                )
                for n in orm_notes
            ]

    def search_by_tags(self, tags: List[str]) -> List[Note]:
        """
        Search for notes that are associated with any of the specified tags.
        :param tags: A list of tag names to search for.
        :return: A list of Note instances matching the query.
        """
        with SessionLocal() as session:
            orm_notes = (
                session.query(NoteORM)
                .join(NoteORM.tags)
                .filter(TagORM.name.in_(tags))
                .distinct()
                .all()
            )

            return [
                Note(
                    id=n.id,
                    title=n.title,
                    content=n.content,
                    tags=[t.name for t in n.tags],
                    created_at=n.created_at,
                    modified_at=n.modified_at,
                )
                for n in orm_notes
            ]
