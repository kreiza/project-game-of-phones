#!/usr/bin/env python
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from db.database import init_db
from src.models.note import Note
from src.models.record import Contact
from src.repositories.contact import ContactRepository
from src.repositories.note import NoteRepository

console = Console()


# ------------------------------
# HELPER FUNCTIONS FOR FORMATTING
# ------------------------------
def display_contact(contact: Contact) -> None:
    """Display a single contact in a nicely formatted panel."""
    info = (
        f"[bold bright_cyan]ID:[/bold bright_cyan] {contact.id}\n"
        f"[bold bright_magenta]Name:[/bold bright_magenta] {contact.name}\n"
        f"[bold bright_green]Phone:[/bold bright_green] {contact.phone_number}\n"
        f"[bold bright_yellow]Email:[/bold bright_yellow] {contact.email}\n"
        f"[bold bright_blue]Address:[/bold bright_blue] {contact.address}\n"
        f"[bold bright_white]Birthday:[/bold bright_white] {contact.birthday}\n"
        f"[bold bright_red]Note:[/bold bright_red] {contact.contact_note or ''}"
    )
    console.print(
        Panel(
            info,
            title="[bold blue]Contact Details[/bold blue]",
            border_style="bright_blue",
        )
    )


def display_note(note: Note) -> None:
    """Display a single note in a nicely formatted panel."""
    tags = ", ".join(note.tags)
    info = (
        f"[bold bright_cyan]ID:[/bold bright_cyan] {note.id}\n"
        f"[bold bright_magenta]Title:[/bold bright_magenta] {note.title}\n"
        f"[bold bright_green]Content:[/bold bright_green] {note.content}\n"
        f"[bold bright_yellow]Tags:[/bold bright_yellow] {tags}\n"
        f"[bold bright_white]Created At:[/bold bright_white] {note.created_at}\n"
        f"[bold bright_white]Modified At:[/bold bright_white] {note.modified_at}"
    )
    console.print(
        Panel(
            info,
            title="[bold green]Note Details[/bold green]",
            border_style="bright_green",
        )
    )


# ------------------------------
# CONTACTS OPERATIONS
# ------------------------------
def add_contact(contact_repo: ContactRepository):
    console.print("[bold green]Add Contact[/bold green]")
    while True:
        name = Prompt.ask("Enter name")
        phone_number = Prompt.ask("Enter phone number")
        address = Prompt.ask("Enter address")
        email = Prompt.ask("Enter email")
        birthday_str = Prompt.ask("Enter birthday (YYYY-MM-DD)")
        contact_note = Prompt.ask("Enter quick note (optional)", default="")

        try:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
            # Create the Contact instance (Pydantic will validate here)
            new_contact = Contact(
                name=name,
                phone_number=phone_number,
                address=address,
                email=email,
                birthday=birthday,
                contact_note=contact_note,
            )
            break  # Exit loop if validation succeeds.
        except Exception as e:
            console.print(f"[red]Validation error: {e}[/red]")
            console.print("[red]Please reenter the contact details.[/red]")

    added = contact_repo.add(new_contact)
    console.print("[bold green]Contact added successfully![/bold green]")
    display_contact(added)


def list_contacts(contact_repo: ContactRepository):
    contacts = contact_repo.list_all()
    if not contacts:
        console.print("[red]No contacts found.[/red]")
        return

    table = Table(title="Contacts", show_lines=True, title_style="bold bright_magenta")
    table.add_column("ID", style="bold cyan", justify="right")
    table.add_column("Name", style="bold magenta")
    table.add_column("Phone", style="bold green")
    table.add_column("Email", style="bold yellow")
    table.add_column("Birthday", style="bold blue")
    table.add_column("Note", style="bold red")
    for c in contacts:
        table.add_row(
            str(c.id),
            c.name,
            c.phone_number,
            c.email,
            str(c.birthday),
            c.contact_note or "",
        )
    console.print(table)


def search_contact_by_id(contact_repo: ContactRepository):
    id_str = Prompt.ask("Enter contact ID")
    try:
        contact_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return
    contact = contact_repo.get_by_id(contact_id)
    if contact:
        console.print("[bold green]Contact found:[/bold green]")
        display_contact(contact)
    else:
        console.print("[red]Contact not found.[/red]")


def search_contact_by_name(contact_repo: ContactRepository):
    name = Prompt.ask("Enter name to search")
    contacts = contact_repo.search_by_name(name)
    if contacts:
        table = Table(
            title=f"Contacts matching '{name}'",
            show_lines=True,
            title_style="bold bright_magenta",
        )
        table.add_column("ID", style="bold cyan", justify="right")
        table.add_column("Name", style="bold magenta")
        table.add_column("Phone", style="bold green")
        table.add_column("Email", style="bold yellow")
        table.add_column("Birthday", style="bold blue")
        table.add_column("Note", style="bold red")
        for c in contacts:
            table.add_row(
                str(c.id),
                c.name,
                c.phone_number,
                c.email,
                str(c.birthday),
                c.contact_note or "",
            )
        console.print(table)
    else:
        console.print("[red]No contacts found with that name.[/red]")


def search_contact_by_birthday(contact_repo: ContactRepository):
    days_str = Prompt.ask("Enter number of days from today for birthday search")
    try:
        days = int(days_str)
    except ValueError:
        console.print("[red]Invalid number[/red]")
        return
    contacts = contact_repo.search_by_birthday_after(days)
    if contacts:
        table = Table(
            title=f"Contacts with birthday {days} days from today",
            show_lines=True,
            title_style="bold bright_magenta",
        )
        table.add_column("ID", style="bold cyan", justify="right")
        table.add_column("Name", style="bold magenta")
        table.add_column("Phone", style="bold green")
        table.add_column("Email", style="bold yellow")
        table.add_column("Birthday", style="bold blue")
        table.add_column("Note", style="bold red")
        for c in contacts:
            table.add_row(
                str(c.id),
                c.name,
                c.phone_number,
                c.email,
                str(c.birthday),
                c.contact_note or "",
            )
        console.print(table)
    else:
        console.print("[red]No contacts found with that birthday.[/red]")


def update_contact(contact_repo: ContactRepository):
    id_str = Prompt.ask("Enter contact ID to update")
    try:
        contact_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return

    updates = {}
    # Let user choose which fields to modify
    while True:
        console.print("\n[bold blue]Which field do you want to modify?[/bold blue]")
        console.print("1. Name")
        console.print("2. Phone Number")
        console.print("3. Address")
        console.print("4. Email")
        console.print("5. Birthday")
        console.print("6. Quick Note")
        console.print("7. Done")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            new_name = Prompt.ask("Enter new name")
            updates["name"] = new_name
        elif choice == "2":
            new_phone = Prompt.ask("Enter new phone number")
            updates["phone_number"] = new_phone
        elif choice == "3":
            new_address = Prompt.ask("Enter new address")
            updates["address"] = new_address
        elif choice == "4":
            new_email = Prompt.ask("Enter new email")
            updates["email"] = new_email
        elif choice == "5":
            new_birthday_str = Prompt.ask("Enter new birthday (YYYY-MM-DD)")
            try:
                new_birthday = datetime.strptime(new_birthday_str, "%Y-%m-%d").date()
                updates["birthday"] = new_birthday
            except Exception as e:
                console.print(
                    f"[red]Invalid date format: {e}. Skipping birthday update.[/red]"
                )
        elif choice == "6":
            new_note = Prompt.ask("Enter new quick note")
            updates["contact_note"] = new_note
        elif choice == "7":
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

    # Attempt to update the contact using the collected updates.
    while True:
        try:
            updated = contact_repo.update(contact_id, updates)
            if updated:
                console.print("[bold green]Contact updated successfully![/bold green]")
                display_contact(updated)
            else:
                console.print("[red]Contact not found or update failed.[/red]")
            break
        except Exception as e:
            console.print(f"[red]Validation error during update: {e}[/red]")
            updates = {}  # Clear existing updates and re-prompt.
            console.print(
                "[red]Please reenter the update information for the contact.[/red]"
            )
            # Re-run update selection loop for contact.
            while True:
                console.print(
                    "\n[bold blue]Which field do you want to modify?[/bold blue]"
                )
                console.print("1. Name")
                console.print("2. Phone Number")
                console.print("3. Address")
                console.print("4. Email")
                console.print("5. Birthday")
                console.print("6. Quick Note")
                console.print("7. Done")
                choice = Prompt.ask("Enter your choice")
                if choice == "1":
                    new_name = Prompt.ask("Enter new name")
                    updates["name"] = new_name
                elif choice == "2":
                    new_phone = Prompt.ask("Enter new phone number")
                    updates["phone_number"] = new_phone
                elif choice == "3":
                    new_address = Prompt.ask("Enter new address")
                    updates["address"] = new_address
                elif choice == "4":
                    new_email = Prompt.ask("Enter new email")
                    updates["email"] = new_email
                elif choice == "5":
                    new_birthday_str = Prompt.ask("Enter new birthday (YYYY-MM-DD)")
                    try:
                        new_birthday = datetime.strptime(
                            new_birthday_str, "%Y-%m-%d"
                        ).date()
                        updates["birthday"] = new_birthday
                    except Exception as e:
                        console.print(
                            f"[red]Invalid date format: {e}. Skipping birthday update.[/red]"
                        )
                elif choice == "6":
                    new_note = Prompt.ask("Enter new quick note")
                    updates["contact_note"] = new_note
                elif choice == "7":
                    break
                else:
                    console.print("[red]Invalid option. Please try again.[/red]")
            # End inner loop and try update again.


def delete_contact(contact_repo: ContactRepository):
    id_str = Prompt.ask("Enter contact ID to delete")
    try:
        contact_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return
    success = contact_repo.delete(contact_id)
    if success:
        console.print(
            f"[bold green]Contact with ID {contact_id} deleted successfully.[/bold green]"
        )
    else:
        console.print("[red]Contact not found or deletion failed.[/red]")


def contacts_menu(contact_repo: ContactRepository):
    while True:
        console.print("\n[bold blue]Contacts Menu[/bold blue]")
        console.print("1. Add contact")
        console.print("2. List all contacts")
        console.print("3. Search contact by ID")
        console.print("4. Search contact by name")
        console.print("5. Search contact by birthday after x days")
        console.print("6. Update contact")
        console.print("7. Delete contact")
        console.print("8. Return to main menu")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            add_contact(contact_repo)
        elif choice == "2":
            list_contacts(contact_repo)
        elif choice == "3":
            search_contact_by_id(contact_repo)
        elif choice == "4":
            search_contact_by_name(contact_repo)
        elif choice == "5":
            search_contact_by_birthday(contact_repo)
        elif choice == "6":
            update_contact(contact_repo)
        elif choice == "7":
            delete_contact(contact_repo)
        elif choice == "8":
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")


# ------------------------------
# NOTES OPERATIONS
# ------------------------------
def add_note(note_repo: NoteRepository):
    console.print("[bold green]Add Note[/bold green]")
    while True:
        title = Prompt.ask("Enter note title")
        content = Prompt.ask("Enter note content")
        tags_str = Prompt.ask("Enter tags (comma separated)", default="")
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        try:
            new_note = Note(title=title, content=content, tags=tags)
            break
        except Exception as e:
            console.print(f"[red]Validation error: {e}[/red]")
            console.print("[red]Please reenter the note details.[/red]")
    added = note_repo.add(new_note)
    console.print("[bold green]Note added successfully![/bold green]")
    display_note(added)


def list_notes(note_repo: NoteRepository):
    notes = note_repo.list_all()
    if not notes:
        console.print("[red]No notes found.[/red]")
        return

    table = Table(title="Notes", show_lines=True, title_style="bold bright_magenta")
    table.add_column("ID", style="bold cyan", justify="right")
    table.add_column("Title", style="bold magenta")
    table.add_column("Content", style="bold green")
    table.add_column("Tags", style="bold yellow")
    table.add_column("Created At", style="bold blue")
    table.add_column("Modified At", style="bold white")
    for n in notes:
        table.add_row(
            str(n.id),
            n.title,
            n.content or "",
            ", ".join(n.tags),
            str(n.created_at),
            str(n.modified_at),
        )
    console.print(table)


def search_note_by_id(note_repo: NoteRepository):
    id_str = Prompt.ask("Enter note ID")
    try:
        note_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return
    note = note_repo.get_by_id(note_id)
    if note:
        console.print("[bold green]Note found:[/bold green]")
        display_note(note)
    else:
        console.print("[red]Note not found.[/red]")


def search_note_by_title(note_repo: NoteRepository):
    title = Prompt.ask("Enter title keyword to search")
    notes = note_repo.search_by_title(title)
    if notes:
        table = Table(
            title=f"Notes matching '{title}'",
            show_lines=True,
            title_style="bold bright_magenta",
        )
        table.add_column("ID", style="bold cyan", justify="right")
        table.add_column("Title", style="bold magenta")
        table.add_column("Content", style="bold green")
        table.add_column("Tags", style="bold yellow")
        table.add_column("Created At", style="bold blue")
        table.add_column("Modified At", style="bold white")
        for n in notes:
            table.add_row(
                str(n.id),
                n.title,
                n.content or "",
                ", ".join(n.tags),
                str(n.created_at),
                str(n.modified_at),
            )
        console.print(table)
    else:
        console.print("[red]No notes found with that title.[/red]")


def search_note_by_tags(note_repo: NoteRepository):
    tags_str = Prompt.ask("Enter tags to search (comma separated)")
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    notes = note_repo.search_by_tags(tags)
    if notes:
        table = Table(
            title="Notes matching tags",
            show_lines=True,
            title_style="bold bright_magenta",
        )
        table.add_column("ID", style="bold cyan", justify="right")
        table.add_column("Title", style="bold magenta")
        table.add_column("Content", style="bold green")
        table.add_column("Tags", style="bold yellow")
        table.add_column("Created At", style="bold blue")
        table.add_column("Modified At", style="bold white")
        for n in notes:
            table.add_row(
                str(n.id),
                n.title,
                n.content or "",
                ", ".join(n.tags),
                str(n.created_at),
                str(n.modified_at),
            )
        console.print(table)
    else:
        console.print("[red]No notes found for those tags.[/red]")


def update_note(note_repo: NoteRepository):
    id_str = Prompt.ask("Enter note ID to update")
    try:
        note_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return

    updates = {}
    # Let the user choose which note fields to update.
    while True:
        console.print(
            "\n[bold blue]Which field do you want to modify in the note?[/bold blue]"
        )
        console.print("1. Title")
        console.print("2. Content")
        console.print("3. Tags")
        console.print("4. Done")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            new_title = Prompt.ask("Enter new title")
            updates["title"] = new_title
        elif choice == "2":
            new_content = Prompt.ask("Enter new content")
            updates["content"] = new_content
        elif choice == "3":
            new_tags_str = Prompt.ask("Enter new tags (comma separated)")
            updates["tags"] = [
                tag.strip() for tag in new_tags_str.split(",") if tag.strip()
            ]
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

    # Attempt to update the note.
    while True:
        try:
            updated = note_repo.update(note_id, updates)
            if updated:
                console.print("[bold green]Note updated successfully![/bold green]")
                display_note(updated)
            else:
                console.print("[red]Note not found or update failed.[/red]")
            break
        except Exception as e:
            console.print(f"[red]Validation error during note update: {e}[/red]")
            updates = {}
            console.print(
                "[red]Please reenter the update information for the note.[/red]"
            )
            # Re-run update selection loop for note.
            while True:
                console.print(
                    "\n[bold blue]Which field do you want to modify in the note?[/bold blue]"
                )
                console.print("1. Title")
                console.print("2. Content")
                console.print("3. Tags")
                console.print("4. Done")
                choice = Prompt.ask("Enter your choice")
                if choice == "1":
                    new_title = Prompt.ask("Enter new title")
                    updates["title"] = new_title
                elif choice == "2":
                    new_content = Prompt.ask("Enter new content")
                    updates["content"] = new_content
                elif choice == "3":
                    new_tags_str = Prompt.ask("Enter new tags (comma separated)")
                    updates["tags"] = [
                        tag.strip() for tag in new_tags_str.split(",") if tag.strip()
                    ]
                elif choice == "4":
                    break
                else:
                    console.print("[red]Invalid option. Please try again.[/red]")
            # End inner loop and try update again.


def delete_note(note_repo: NoteRepository):
    id_str = Prompt.ask("Enter note ID to delete")
    try:
        note_id = int(id_str)
    except ValueError:
        console.print("[red]Invalid ID[/red]")
        return
    success = note_repo.delete(note_id)
    if success:
        console.print(
            f"[bold green]Note with ID {note_id} deleted successfully.[/bold green]"
        )
    else:
        console.print("[red]Note not found or deletion failed.[/red]")


def notes_menu(note_repo: NoteRepository):
    while True:
        console.print("\n[bold blue]Notes Menu[/bold blue]")
        console.print("1. Add note")
        console.print("2. List all notes")
        console.print("3. Search note by ID")
        console.print("4. Search note by title")
        console.print("5. Search note by tags")
        console.print("6. Update note")
        console.print("7. Delete note")
        console.print("8. Return to main menu")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            add_note(note_repo)
        elif choice == "2":
            list_notes(note_repo)
        elif choice == "3":
            search_note_by_id(note_repo)
        elif choice == "4":
            search_note_by_title(note_repo)
        elif choice == "5":
            search_note_by_tags(note_repo)
        elif choice == "6":
            update_note(note_repo)
        elif choice == "7":
            delete_note(note_repo)
        elif choice == "8":
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")


# ------------------------------
# MAIN MENU
# ------------------------------
def main():
    init_db()
    contact_repo = ContactRepository()
    note_repo = NoteRepository()
    while True:
        console.print("\n[bold green]Main Menu[/bold green]")
        console.print("1. Contacts operations")
        console.print("2. Notes operations")
        console.print("3. Exit")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            contacts_menu(contact_repo)
        elif choice == "2":
            notes_menu(note_repo)
        elif choice == "3":
            console.print("[bold green]Goodbye![/bold green]")
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")


if __name__ == "__main__":
    main()
