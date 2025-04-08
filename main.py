from models.note import Note


def show_note_commands():
    commands = [
        "add note",
        "edit note",
        "delete note",
        "show note",
        "show all",
        "add tag",
        "edit tag",
        "search by tag",
        "commands",
        "close or exit",
    ]
    return "Available commands:\n 👉 " + "\n 👉 ".join(commands)



def main():
    print(show_note_commands())
    while True:
        user_input = input("Enter a command:")
        command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
                print("Good bye!")
                break

if __name__ == "__main__":
    main()