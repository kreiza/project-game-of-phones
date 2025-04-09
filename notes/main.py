from models import Note, NoteBook


def parse_input(user_input):
    return user_input.strip().lower()

def show_note_commands():
    commands = [
        "add note",
        "edit note",
        "delete note",
        "show note",
        "show all notes",
        "search",
        "add tag",
        "edit tag",
        'delete tag',
        "search by tag",
        "commands",
        "close or exit",
    ]
    return "Available commands:\n 👉 " + "\n 👉 ".join(commands)


def add_note(self):
    try:
        name = input("Enter a note title: ").strip()
        if not name:
            print("Note title is required.")
            return 
        
        content = input("Enter note content: ").strip()
        record = Note(name, content)

        while True:
            choice = input("Add a tag to this note? (y/n): ").strip().lower()
            if choice != 'y':
                break

            tag = input("Enter tag: ").strip()
            if tag:
                try:
                    record.add_tag(tag)
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Empty tag skipped.")

        self.add_note(record)
        print(f"\n✅ Note '{name}' added successfully!")

    except Exception as e:
        print(f"❌ Something went wrong: {e}")




def main():
    notebook = NoteBook()
    print(show_note_commands())
    while True:
        user_input = input("Enter a command:")
        command = parse_input(user_input)

        if command == "add note":
            add_note(notebook)


        if command in ["close", "exit"]:
            print("Good bye!")
            break

        else:
            print("⚠️ Unknown command. Type 'commands' to see available ones.")

if __name__ == "__main__":
    main()