import argparse
import argcomplete

from db.database import init_db
from src.cli_records import run_records_cli
from src.cli_notes import run_notes_cli


def main() -> None:
    """
    Main entry point for the Phonebook application (interactive mode).

    At the top level, the user chooses a module ('record' or 'note').
    The remaining command-line arguments are then passed to the appropriate sub-parser.
    """
    # Ensure the database is initialized.
    init_db()

    # Create the top-level parser.
    parser = argparse.ArgumentParser(
        description="Phonebook CLI Application (interactive mode)"
    )
    subparsers = parser.add_subparsers(dest="module", help="Module to run", required=True)

    # Sub-parser for record operations.
    record_parser = subparsers.add_parser("record", help="Record operations")
    record_parser.set_defaults(func=run_records_cli)

    # Sub-parser for note operations.
    note_parser = subparsers.add_parser("note", help="Note operations")
    note_parser.set_defaults(func=run_notes_cli)

    argcomplete.autocomplete(parser)
    # Parse known arguments and collect the rest.
    args, remaining_argv = parser.parse_known_args()

    if hasattr(args, "func"):
        # Pass the remaining arguments to the chosen module's CLI handler.
        args.func(remaining_argv)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
