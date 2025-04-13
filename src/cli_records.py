import argparse
import argcomplete
from datetime import date
from typing import Any

from src.models.record import PhoneBookRecord
from src.repositories.record import PhoneBookRecordRepository

def add_record(args: argparse.Namespace) -> None:
    name = args.name if args.name is not None else input("Please, enter the name: ")
    phone = args.phone if args.phone is not None else input("Please, enter the phone number: ")
    address = args.address if args.address is not None else input("Please, enter the address: ")
    email = args.email if args.email is not None else input("Please, enter the email: ")
    birthday_str = args.birthday if args.birthday is not None else input("Please, enter the birthday (YYYY-MM-DD): ")
    notes = args.notes if args.notes is not None else input("Please, enter additional notes (optional): ")

    try:
        birthday_date = date.fromisoformat(birthday_str)
    except ValueError as ve:
        print(f"Invalid birthday format: {ve}")
        return

    try:
        record = PhoneBookRecord(
            name=name,
            phone_number=phone,
            address=address,
            email=email,
            birthday=birthday_date,
            notes=notes if notes.strip() != "" else None
        )
    except Exception as e:
        print(f"Error creating record: {e}")
        return

    repo = PhoneBookRecordRepository()
    added_record = repo.add(record)
    print(f"Added record with ID {added_record.id}")

def list_records(args: argparse.Namespace) -> None:
    repo = PhoneBookRecordRepository()
    records = repo.list_all()
    if not records:
        print("No records found.")
    else:
        for rec in records:
            print(rec.json())

def update_record(args: argparse.Namespace) -> None:
    record_id = args.id if args.id is not None else int(input("Please, enter the record ID to update: "))
    new_name = args.name if args.name is not None else input("Please, enter the new name (leave blank to keep unchanged): ")
    new_phone = args.phone if args.phone is not None else input("Please, enter the new phone number (leave blank to keep unchanged): ")
    new_address = args.address if args.address is not None else input("Please, enter the new address (leave blank to keep unchanged): ")
    new_email = args.email if args.email is not None else input("Please, enter the new email (leave blank to keep unchanged): ")
    new_birthday_str = args.birthday if args.birthday is not None else input("Please, enter the new birthday (YYYY-MM-DD, leave blank to keep unchanged): ")
    new_notes = args.notes if args.notes is not None else input("Please, enter the new additional notes (leave blank to keep unchanged): ")

    updates: dict[str, Any] = {}
    if new_name.strip():
        updates["name"] = new_name.strip()
    if new_phone.strip():
        updates["phone_number"] = new_phone.strip()
    if new_address.strip():
        updates["address"] = new_address.strip()
    if new_email.strip():
        updates["email"] = new_email.strip()
    if new_birthday_str.strip():
        try:
            updates["birthday"] = date.fromisoformat(new_birthday_str.strip())
        except ValueError as ve:
            print(f"Invalid birthday format: {ve}")
            return
    if new_notes.strip():
        updates["notes"] = new_notes.strip()

    repo = PhoneBookRecordRepository()
    updated_record = repo.update(record_id, updates)
    if updated_record:
        print("Record updated:")
        print(updated_record.json())
    else:
        print(f"No record found with ID {record_id}")

def delete_record(args: argparse.Namespace) -> None:
    record_id = args.id if args.id is not None else int(input("Please, enter the record ID to delete: "))
    confirm = input(f"Are you sure you want to delete record {record_id}? (y/n): ").lower()
    if confirm == 'y':
        repo = PhoneBookRecordRepository()
        success = repo.delete(record_id)
        if success:
            print(f"Record with ID {record_id} deleted successfully.")
        else:
            print(f"No record found with ID {record_id}")
    else:
        print("Deletion cancelled.")

def run_records_cli(argv=None) -> None:
    """
    Set up the interactive CLI parser for phonebook record commands.
    """
    parser = argparse.ArgumentParser(description="Phonebook Record CLI (interactive mode)")
    subparsers = parser.add_subparsers(dest="command", help="Available record commands", required=True)

    # add_record command.
    parser_add = subparsers.add_parser("add_record", help="Add a new record interactively")
    parser_add.add_argument("--name", help="Name", default=None)
    parser_add.add_argument("--phone", help="Phone number", default=None)
    parser_add.add_argument("--address", help="Address", default=None)
    parser_add.add_argument("--email", help="Email", default=None)
    parser_add.add_argument("--birthday", help="Birthday (YYYY-MM-DD)", default=None)
    parser_add.add_argument("--notes", help="Additional notes", default=None)
    parser_add.set_defaults(func=add_record)

    # list_records command.
    parser_list = subparsers.add_parser("list_records", help="List all records")
    parser_list.set_defaults(func=list_records)

    # update_record command.
    parser_update = subparsers.add_parser("update_record", help="Update a record interactively")
    parser_update.add_argument("--id", type=int, help="Record ID", default=None)
    parser_update.add_argument("--name", help="New name", default=None)
    parser_update.add_argument("--phone", help="New phone number", default=None)
    parser_update.add_argument("--address", help="New address", default=None)
    parser_update.add_argument("--email", help="New email", default=None)
    parser_update.add_argument("--birthday", help="New birthday (YYYY-MM-DD)", default=None)
    parser_update.add_argument("--notes", help="New additional notes", default=None)
    parser_update.set_defaults(func=update_record)

    # delete_record command.
    parser_delete = subparsers.add_parser("delete_record", help="Delete a record interactively")
    parser_delete.add_argument("--id", type=int, help="Record ID", default=None)
    parser_delete.set_defaults(func=delete_record)

    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    run_records_cli()