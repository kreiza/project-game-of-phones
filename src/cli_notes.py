import argparse
import argcomplete
from typing import Any

from src.models.note import Note
from src.repositories.note import NoteRepository


def get_arg_or_input(arg_value, prompt: str, optional: bool = False) -> str | None:
    if arg_value is not None:
        return arg_value
    user_input = input(prompt).strip()
    return user_input if user_input or not optional else None


def add_note(args: argparse.Namespace) -> None:
    title = get_arg_or_input(args.title, "Please, enter the note title: ")
    content = get_arg_or_input(args.content, "Enter note content (optional, press Enter to skip): ", optional=True)

    tags_input = get_arg_or_input(args.tags, "Please, enter the tags (comma separated): ", optional=True)
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []

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
        print(f"🗒️ Listing {len(notes)} note(s):")
        for note in notes:
            print(note.json())


def update_note(args: argparse.Namespace) -> None:
    try:
        note_id = args.id if args.id is not None else int(input("Please, enter the note ID to update: "))
    except ValueError:
        print("❌ Invalid ID. Must be a number.")
        return
    
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
    try:
        note_id = args.id if args.id is not None else int(input("Please, enter the note ID to delete: "))
    except ValueError:
        print("❌ Invalid ID. Must be a number.")
        return

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


def search_notes(args: argparse.Namespace) -> None:
    """
    Search notes by title only.
    """
    title_input = args.title if args.title is not None else input(
        "Enter the title to search: ").strip()
    title = title_input if title_input else None

    if not title:
        print("❌ You must provide a title to search.")
        return

    repo = NoteRepository()
    notes = repo.search_by_title(title)

    if not notes:
        print("🔍 No matching notes found.")
    else:
        print(f"🔎 Found {len(notes)} note(s):")
        for note in notes:
            print(f"ID: {note.id}\nTitle: {note.title}\nTags: {', '.join(note.tags)}\n---")


def search_notes_by_tag(args: argparse.Namespace) -> None:
    tags_input = args.tags if args.tags is not None else input("Please, enter the tags to search (comma separated): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input.strip() != "" else []
    repo = NoteRepository()
    notes = repo.search_by_tags(tags)
    if not notes:
        print("🔍 No matching notes found.")
    else:
        print(f"🔎 Found {len(notes)} note(s):")
        for note in notes:
            print(f"ID: {note.id}\nTitle: {note.title}\nTags: {', '.join(note.tags)}\n---")


def run_notes_cli(argv=None) -> None:
    """
    Set up the interactive CLI parser for note commands.
    """
    parser = argparse.ArgumentParser(description="Notes CLI (interactive mode)")
    subparsers = parser.add_subparsers(dest="command", help="Available note commands", required=True)

    parser_add = subparsers.add_parser("add_note", help="Add a new note")
    parser_add.add_argument("--title", help="Title of the note", default=None)
    parser_add.add_argument("--content", help="Content of the note", default=None)
    parser_add.add_argument("--tags", help="Comma separated list of tags", default=None)
    parser_add.set_defaults(func=add_note)

    parser_list = subparsers.add_parser("list_notes", help="List all notes")
    parser_list.set_defaults(func=list_notes)

    parser_update = subparsers.add_parser("update_note", help="Update an existing note")
    parser_update.add_argument("--id", type=int, help="Note ID", default=None)
    parser_update.add_argument("--title", help="New title for the note", default=None)
    parser_update.add_argument("--content", help="New content for the note", default=None)
    parser_update.add_argument("--tags", help="New comma separated list of tags", default=None)
    parser_update.set_defaults(func=update_note)

    parser_delete = subparsers.add_parser("delete_note", help="Delete a note")
    parser_delete.add_argument("--id", type=int, help="Note ID", default=None)
    parser_delete.set_defaults(func=delete_note)

    parser_search_title = subparsers.add_parser("search_by_title", help="Search notes by title")
    parser_search_title.add_argument("--title", help="Search by title", default=None)
    parser_search_title.set_defaults(func=search_notes)

    parser_search_tags = subparsers.add_parser("search_by_tags", help="Search notes by tags")
    parser_search_tags.add_argument("--tags", help="Comma separated list of tags to search", default=None)
    parser_search_tags.set_defaults(func=search_notes_by_tag)

    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()



if __name__ == "__main__":
    run_notes_cli()