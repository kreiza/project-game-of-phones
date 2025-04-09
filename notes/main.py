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
        "delete tag",
        "search by tag",
        "commands",
        "close or exit",
    ]
    return "Available commands:\n 👉 " + "\n 👉 ".join(commands)


def add_note(self):
    try:
        while True:
            title = input("Enter a note title (or type 'exit' to cancel): ").strip()
            if title.lower() == "exit":
                print("Note creation canceled.")
                return
            if not title:
                print("Note title is required. Please enter a title.")
            else:
                break

        content = input("Enter note content: ").strip()
        record = Note(title, content)

        while True:
            choice = input("Add a tag to this note? (y/n): ").strip().lower()
            if choice != "y":
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
        print(f"\n✅ Note '{title}' added successfully!")

    except Exception as e:
        print(f"❌ Something went wrong: {e}")


def edit_note(self):
    try:
        while True:
            title = input("Enter a note title (or type 'exit' to cancel): ").strip()
            if title.lower() == "exit":
                print("Note creation canceled.")
                return
            if not title:
                print("Note title is required. Please enter a title.")
            else:
                break


        note_to_find = self.find_note(title)
        if not note_to_find:
            print("Note with this title doesn't exist.")
            return

        new_title = input(f"Enter new title for '{title}' (leave empty to keep the current title): ").strip()
        
        if not new_title:
            new_title = title

        new_content = input(f"Enter new content for '{title}': ").strip()

        note_to_find.edit_note(new_title, new_content)

        if new_title != title:
            self.data.pop(title)
        self.data[new_title] = note_to_find

        print(f"✅ Note '{new_title}' edited successfully!")

    except Exception as e:
        print(f"❌ Something went wrong: {e}")


def show_note(self):
    while True:
        title = input("Enter a note title (or type 'exit' to cancel): ").strip()
        if title.lower() == "exit":
            print("Note creation canceled.")
            return
        if not title:
            print("Note title is required. Please enter a title.")
        else:
            print(self.show_note(title))
            break


def main():
    notebook = NoteBook()
    print(show_note_commands())
    while True:
        user_input = input("Enter a command:")
        command = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "add note":
            add_note(notebook)

        elif command == "edit note":
            edit_note(notebook)

        elif command == "show note":
            show_note(notebook)

        elif command == "show all notes":
            print(notebook.show_all())    

        else:
            print("⚠️ Unknown command. Type 'commands' to see available ones.")


if __name__ == "__main__":
    main()
