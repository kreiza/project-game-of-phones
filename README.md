# Modern Contact and Note Management System with SQLite Backend

A robust Python-based contact and note management system that provides an intuitive interface for organizing contacts and associated notes with tagging capabilities. Built with SQLAlchemy ORM and Rich CLI interface for a seamless user experience.

This application offers a comprehensive solution for managing personal and professional contacts with features like birthday tracking, note organization with tags, and powerful search capabilities. It uses SQLite as its database backend for reliable data persistence and SQLAlchemy ORM for type-safe database operations.

The system implements a clean architecture with repository pattern for data access, providing clear separation of concerns and making the codebase maintainable and extensible. The Rich library delivers a polished command-line interface with colored output and formatted tables for enhanced user experience.

## Repository Structure
```
.
├── db/                          # Database related code
│   ├── database.py             # Database connection and initialization
│   └── orm_models.py           # SQLAlchemy ORM models for data persistence
├── src/
│   ├── common/
│   │   └── repository.py       # Abstract repository pattern implementation
│   ├── models/                 # Domain models
│   │   ├── note.py            # Note entity model
│   │   └── record.py          # Contact entity model
│   ├── repositories/           # Concrete repository implementations
│   │   ├── contact.py         # Contact repository implementation
│   │   └── note.py            # Note repository implementation
│   └── main.py                # Application entry point and CLI interface
└── LICENSE                     # MIT License file
```

## Usage Instructions
### Prerequisites
- Python 3.12 or higher
- pip (Python package installer)
- SQLite 3

Required Python packages:
```
sqlalchemy
rich
pydantic
```

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

1. Initialize the database:
```python
from db.database import init_db
init_db()
```

2. Run the application:
```bash
python src/main.py
```

### More Detailed Examples

1. Adding a new contact:
```python
from src.models.record import Contact
from src.repositories.contact import ContactRepository

contact_repo = ContactRepository()
new_contact = Contact(
    name="John Doe",
    phone_number="+1234567890",
    address="123 Main St",
    email="john@example.com",
    birthday="1990-01-01"
)
contact_repo.add(new_contact)
```

2. Adding a note with tags:
```python
from src.models.note import Note
from src.repositories.note import NoteRepository

note_repo = NoteRepository()
new_note = Note(
    title="Meeting Notes",
    content="Important discussion points...",
    tags=["work", "meeting"]
)
note_repo.add(new_note)
```

### Troubleshooting

1. Database Connection Issues
```
Error: Unable to connect to database
Solution: 
- Verify SQLite is installed
- Check file permissions in the application directory
- Ensure database path is correct in db/database.py
```

2. Data Validation Errors
```
Error: Validation error in contact/note creation
Solution:
- Check input format for dates (YYYY-MM-DD)
- Ensure email addresses are valid
- Verify phone numbers match required format
```

## Data Flow
The application follows a three-layer architecture for data management: presentation, business logic, and data access.

```ascii
[User Input] -> [Rich CLI Interface] -> [Domain Models]
                                          |
                                    [Repositories]
                                          |
                                  [SQLAlchemy ORM]
                                          |
                                    [SQLite DB]
```

Key component interactions:
1. User input is captured and validated through the Rich CLI interface
2. Domain models (Contact, Note) enforce business rules and data validation
3. Repository pattern abstracts database operations
4. SQLAlchemy ORM handles object-relational mapping
5. SQLite provides persistent storage with ACID compliance
6. Tag system enables flexible note organization and searching
7. Contact birthday tracking supports proactive relationship management