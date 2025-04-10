import argparse
import argcomplete
from typing import Any

from src.models.note import Note
from src.repositories.note import NoteRepository


def add_note(args: argparse.Namespace) -> None:
    title = args.title if args.title is not None else input("Please, enter the note title: ")

    content = args.content if hasattr(args, 'content') else None
    if content is None:
        content_input = input("Enter note content (optional, press Enter to skip): ").strip()
        content = content_input if content_input != "" else None

    tags_input = args.tags if args.tags is not None else input("Please, enter the tags (comma separated): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input.strip() != "" else []

    audit_message = f"Note '{title}' was created."

    note = Note(title=title, content=content, tags=tags, audit_message=audit_message)
    repo = NoteRepository()
    added_note = repo.add(note)
    print(f"✅ Added note with ID {added_note.id}")


def list_notes(args: argparse.Namespace) -> None:
    repo = NoteRepository()
    notes = repo.list_all()
    if not notes:
        print("No notes found.")
    else:
        for note in notes:
            print(note.json())


def update_note(args: argparse.Namespace) -> None:
    note_id = args.id if args.id is not None else int(input("Please, enter the note ID to update: "))
    
    new_title = args.title if hasattr(args, 'title') and args.title is not None else input(
        "Please, enter the new note title (leave blank to keep unchanged): ")
    
    new_content = args.content if hasattr(args, 'content') else None
    if new_content is None:
        new_content_input = input("Enter new note content (optional, press Enter to skip): ").strip()
        new_content = new_content_input if new_content_input != "" else None

    tags_input = args.tags if hasattr(args, 'tags') and args.tags is not None else input(
        "Please, enter new tags (comma separated, leave blank to keep unchanged): ")
    new_tags = [tag.strip() for tag in tags_input.split(",")] if tags_input.strip() != "" else []

    updates: dict[str, Any] = {}
    if new_title.strip():
        updates["title"] = new_title.strip()  
    if new_content is not None:
        updates["content"] = new_content  
    if new_tags:
        updates["tags"] = new_tags 
    
    audit_message = f"Note {note_id} was updated."
    updates["audit_message"] = audit_message

    repo = NoteRepository()
    updated_note = repo.update(note_id, updates)
    
    if updated_note:
        print("✅ Note updated:")
        print(updated_note.json())
    else:
        print(f"❌ No note found with ID {note_id}")



def delete_note(args: argparse.Namespace) -> None:
    note_id = args.id if args.id is not None else int(input("Please, enter the note ID to delete: "))

    confirm = input(f"Are you sure you want to delete note {note_id}? (y/n): ").lower()
    if confirm == 'y':
        repo = NoteRepository()
        success = repo.delete(note_id)
        
        if success:
            print(f"✅ Note with ID {note_id} deleted successfully.")
        else:
            print(f"❌ No note found with ID {note_id}")
    else:
        print("❌ Deletion cancelled.")



def search_by_tags  (args: argparse.Namespace) -> None:
    tags_input = args.tags if args.tags is not None else input("Please, enter the tags to search (comma separated): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input.strip() != "" else []
    repo = NoteRepository()
    notes = repo.search_by_tags(tags)
    if not notes:
        print("No matching notes found.")
    else:
        for note in notes:
            print(note.json())



            def search_notes(args: argparse.Namespace) -> None:
    # Get the title to search (optional)
    title_input = args.title if args.title is not None else input("Please, enter the title to search (leave blank to skip): ").strip()
    
    # Get the tags to search (optional)
    tags_input = args.tags if args.tags is not None else input("Please, enter the tags to search (comma separated, leave blank to skip): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input.strip() != "" else []

    # Prepare the search criteria
    search_criteria = {
        'title': title_input if title_input != "" else None,
        'tags': tags if tags else None
    }

    # Perform search using repository
    repo = NoteRepository()
    notes = repo.search(search_criteria)

    # Print search results
    if not notes:
        print("No matching notes found.")
    else:
        for note in notes:
            print(note.json())


def run_notes_cli(argv=None) -> None:
    """
    Set up the interactive CLI parser for note commands.
    """
    parser = argparse.ArgumentParser(description="Notes CLI (interactive mode)")
    subparsers = parser.add_subparsers(dest="command", help="Available note commands", required=True)

    parser_add = subparsers.add_parser("add_note", help="Add a new note")
    parser_add.add_argument("--text", help="Text of the note", default=None)
    parser_add.add_argument("--tags", help="Comma separated list of tags", default=None)
    parser_add.set_defaults(func=add_note)

    parser_list = subparsers.add_parser("list_notes", help="List all notes")
    parser_list.set_defaults(func=list_notes)

    parser_update = subparsers.add_parser("update_note", help="Update an existing note")
    parser_update.add_argument("--id", type=int, help="Note ID", default=None)
    parser_update.add_argument("--text", help="New text for the note", default=None)
    parser_update.add_argument("--tags", help="New comma separated list of tags", default=None)
    parser_update.set_defaults(func=update_note)

    parser_delete = subparsers.add_parser("delete_note", help="Delete a note")
    parser_delete.add_argument("--id", type=int, help="Note ID", default=None)
    parser_delete.set_defaults(func=delete_note)

    parser_search = subparsers.add_parser("search_notes", help="Search notes by tags")
    parser_search.add_argument("--tags", help="Comma separated list of tags to search", default=None)
    parser_search.set_defaults(func=search_notes)

    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    run_notes_cli()