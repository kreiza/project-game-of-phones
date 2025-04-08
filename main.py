from input_error import input_error
from classes import AddressBook, Record
from parse_input import parse_input



@input_error   
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact not found"
    record.add_email(email)
    return f"Email to {name} added"

def add_address(args, book: AddressBook):
    name, *rest = args
    record = book.find(name)
    if record is None:
        return f"Contact not found"
    address = " ".join(rest)
    record.add_address(address)
    return f"Address to {name} added"

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return "Incorrect number of arguments. Use: add-birthday [name] [date of birth]"
    name, birthday = args
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
            return f"Birthday for {name} added."
        except ValueError as e:
            return str(e)
    else:
        return f"Error: Contact {name} not found."

def show_all(book: AddressBook):
    if not book.data:
        return "No contacts available."
    else:
        result = "\n".join(str(record) for record in book.data.values())
        return result



def main():
    book = AddressBook() 

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "all":
                print(show_all(book))   
            case "add-birthday":
                print(add_birthday(args, book))
            case "add-email":
                print(add_email(args, book))
            case "add-address":
                print(add_address(args, book))
            case _:
                print("Invalid command.")

   

if __name__ == "__main__":
    main()