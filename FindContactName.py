 # это шаблон БД

raw_valid_contacts = [
    {"name": "Іван", "phone": "+380-67-123-45-67"},
    {"name": "Анна", "phone": "+380-50-765-43-21"},
    {"name": "Олег", "phone": "+380-93-555-12-34"},
]
 
# класс обработки конкретного человека

class ContactPerson:
    def __init__(self, phone, name):

        self.phone = phone
        self.name = name 
        
    def __str__(self):       

        return f"Name: {self.name}, Phone: {self.phone}"
    
class PhoneBookFind:
    def __init__(self, raw_valid_contacts):

        self.local_contacts_database = raw_valid_contacts # локальная БД 
    
    def find(self):

        for contact_data in self.local_contacts_database:
             if contact_data["name"].lower() == input_name.lower():  # находим имя
                # если имя найдено, создаем объект ContactPerson
                contact = ContactPerson(contact_data["phone"], contact_data["name"])
                return contact
             
input_name = input(" ") # пример имени введеного для поиска 
find_book = PhoneBookFind(raw_valid_contacts)
found_contact = find_book.find()
# вывод
if found_contact:
    print("Контакт знайден:")

    print(found_contact)  
else:
    print("Контакт не знайден.")
        
        


     