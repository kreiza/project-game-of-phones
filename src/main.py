from src.cli import run_cli
from db.database import init_db

def main() -> None:
    """
    Main entry point for the phonebook CLI application.
    """
    init_db()
    run_cli()

if __name__ == "__main__":
    main()
