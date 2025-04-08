
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
      self.value = value

class Email(Field): 
    def __init__(self, value):
      self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            # Перевіряємо формат і зберігаємо дату як datetime-об'єкт
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
class Address(Field): 
    def __init__(self, value):
      self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def add_email(self, email):
        self.email = (Email(email))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        self.address = (Address(address))
  
    def __str__(self):
        return f"""Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, 
        email: {self.email}, birthday: {self.birthday}, address: {self.address}"""

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record #Додає запис до адресної книги
    def find(self, name):
        return self.data.get(name, None)      #Знаходить запис за ім'ям.

    
 
    

   

