import argparse
from datetime import date

from db.database import init_db
from src.common.models import PhoneBookRecord
from src.repositories.record import PhoneBookRecordRepository


def add_command(args: argparse.Namespace) -> None:
    """
    Handle the add command to create a new phonebook record.
    """
    try:
        birthday_date = date.fromisoformat(args.birthday)
    except ValueError as ve:
        print(f"Invalid birthday format: {ve}")
        return

    try:
        record = PhoneBookRecord(
            name=args.name,
            phone_number=args.phone,
            address=args.address,
            email=args.email,
            birthday=birthday_date,
            notes=args.notes,
        )
    except Exception as e:
        print(f"Error creating record: {e}")
        return

    repo = PhoneBookRecordRepository()
    added_record = repo.add(record)
    print(f"Added record with ID {added_record.id}")


def list_command(args: argparse.Namespace) -> None:
    """
    Handle the list command to display all phonebook records.
    """
    repo = PhoneBookRecordRepository()
    records = repo.list_all()
    if not records:
        print("No records found.")
    else:
        for rec in records:
            print(rec.json())


def update_command(args: argparse.Namespace) -> None:
    """
    Handle the update command to modify an existing phonebook record.
    Only the provided fields will be updated.
    """
    repo = PhoneBookRecordRepository()

    updates = {}
    if args.name:
        updates["name"] = args.name
    if args.phone:
        updates["phone_number"] = args.phone
    if args.address:
        updates["address"] = args.address
    if args.email:
        updates["email"] = args.email
    if args.birthday:
        try:
            updates["birthday"] = date.fromisoformat(args.birthday)
        except ValueError as ve:
            print(f"Invalid birthday format: {ve}")
            return
    if args.notes is not None:  # notes can be an empty string
        updates["notes"] = args.notes

    updated_record = repo.update(args.id, updates)
    if updated_record:
        print("Record updated:")
        print(updated_record.json())
    else:
        print(f"No record found with ID {args.id}")


def delete_command(args: argparse.Namespace) -> None:
    """
    Handle the delete command to remove a phonebook record.
    """
    repo = PhoneBookRecordRepository()
    success = repo.delete(args.id)
    if success:
        print(f"Record with ID {args.id} deleted successfully.")
    else:
        print(f"No record found with ID {args.id}")


def run_cli() -> None:
    """
    Set up the CLI parser and handle commands.
    """
    parser = argparse.ArgumentParser(description="Phonebook CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new phonebook record")
    parser_add.add_argument("--name", required=True, help="Name of the contact")
    parser_add.add_argument("--phone", required=True, help="Phone number")
    parser_add.add_argument("--address", required=True, help="Address")
    parser_add.add_argument("--email", required=True, help="Email address")
    parser_add.add_argument(
        "--birthday", required=True, help="Birthday in YYYY-MM-DD format"
    )
    parser_add.add_argument(
        "--notes", required=False, help="Additional notes", default=None
    )
    parser_add.set_defaults(func=add_command)

    # List command
    parser_list = subparsers.add_parser("list", help="List all phonebook records")
    parser_list.set_defaults(func=list_command)

    # Update command
    parser_update = subparsers.add_parser(
        "update", help="Update an existing phonebook record"
    )
    parser_update.add_argument(
        "--id", type=int, required=True, help="ID of the record to update"
    )
    parser_update.add_argument("--name", help="Updated name")
    parser_update.add_argument("--phone", help="Updated phone number")
    parser_update.add_argument("--address", help="Updated address")
    parser_update.add_argument("--email", help="Updated email address")
    parser_update.add_argument(
        "--birthday", help="Updated birthday in YYYY-MM-DD format"
    )
    parser_update.add_argument("--notes", help="Updated notes")
    parser_update.set_defaults(func=update_command)

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a phonebook record")
    parser_delete.add_argument(
        "--id", type=int, required=True, help="ID of the record to delete"
    )
    parser_delete.set_defaults(func=delete_command)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    # Ensure the database is initialized before running any command.
    init_db()
    run_cli()
