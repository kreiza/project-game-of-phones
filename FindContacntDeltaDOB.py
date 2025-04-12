import datetime
# шабло БД с ДР
raw_valid_contacts = [
    {"name": "Іван Іванов", "dob": "1995-03-12"},
    {"name": "Марія Петрова", "dob": "1988-07-25"},
    {"name": "Олексій Смирнов", "dob": "2000-01-15"},
    {"name": "Олена Васильєва", "dob": "1992-09-03"},
    {"name": "Дмитро Козлов", "dob": "1985-04-17"}
]

class ContactPersonDOB:
    def __init__(self, dob, name):
        self.dob = dob
        self.name = name
        
    def __str__(self):       
        return f"Name: {self.name}, Birthday: {self.dob}"

class PhoneBookFindDOB:
    def __init__(self, raw_valid_contacts):
        self.local_contacts_database = raw_valid_contacts
           
    def find_dob(self, new_date):
        for contact_data in self.local_contacts_database:
            contact_dob = datetime.datetime.strptime(contact_data["dob"], "%Y-%m-%d").date()
            if contact_dob.month == new_date.month and contact_dob.day == new_date.day:
                contact = ContactPersonDOB(contact_dob, contact_data["name"])
                return contact
        return None

current_date = datetime.date.today()
input_days_to_add = int(input("Введите количество дней для поиска: "))
new_date = current_date + datetime.timedelta(days=input_days_to_add)

find_book_dob = PhoneBookFindDOB(raw_valid_contacts)
found_contact = find_book_dob.find_dob(new_date)

if found_contact:
    print(f"День народження через {input_days_to_add} днів буде у {found_contact}")
else:
    print("Контакт не знайдено.")
