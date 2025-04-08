import string

class ErrorsCheck:
    def __init__(self, phone_number_str=None, email_address_str=None):
        self.phone_number_str = phone_number_str
        self.email_address_str = email_address_str
        self.errors = []

    # Проверка номера телефона
    def validate_phone_number(self):
        if self.phone_number_str is None:
            self.errors.append("Номер телефону не надано.")
            return

        if not isinstance(self.phone_number_str, str):
            self.errors.append("Помилка: Очікувався рядок (string).")
            return

        if not self.phone_number_str:
            self.errors.append("Номер телефону не може бути порожнім.")
            return

        allowed_chars = {'+', '-', '(', ')', ' '}.union(set(string.digits))
        has_invalid_char = False
        for char in self.phone_number_str:
            if char not in allowed_chars:
                has_invalid_char = True
                break

        if has_invalid_char:
            self.errors.append("Ви використовували неприпустимий символ у номері телефону.")

        digits_only = ''.join(filter(str.isdigit, self.phone_number_str))
        if not digits_only and self.phone_number_str:
            self.errors.append("У номері телефону мають бути цифри.")

        MIN_DIGIT_LEN = 7
        MAX_DIGIT_LEN = 15

        if digits_only:
            if len(digits_only) < MIN_DIGIT_LEN:
                self.errors.append(f"Номер телефону надто короткий (мінімум {MIN_DIGIT_LEN} цифр).")
            if len(digits_only) > MAX_DIGIT_LEN:
                self.errors.append(f"Номер телефону надто довгий (максимум {MAX_DIGIT_LEN} цифр).")

        if '+' in self.phone_number_str and self.phone_number_str.find('+') != 0:
            self.errors.append("Символ '+' дозволено лише на початку номера.")

    # Проверка email
    def validate_email_address(self):
        if self.email_address_str is None:
            self.errors.append("Email адреса не надана.")
            return

        if not isinstance(self.email_address_str, str):
            self.errors.append("Помилка: Очікувався рядок (string).")
            return

        if not self.email_address_str:
            self.errors.append("Email адреса не може бути порожньою.")
            return

        if self.email_address_str.count('@') != 1:
            self.errors.append("Email адреса повинна містити рівно один символ '@'.")
            return

        local_part, domain_part = self.email_address_str.split('@', 1)

        if not local_part:
            self.errors.append("Email повинен містити символ '@'.")
            return

        if not domain_part:
            self.errors.append("Повинен бути хоча б один символ після '@'.")
            return

        if '.' not in domain_part:
            self.errors.append("Після '@' повинна бути хоча б одна крапка '.'.")

    # Функция для вывода всех ошибок
    def output_errors(self):
        self.validate_phone_number()
        self.validate_email_address()
        return self.errors

def run_validation(phone_number_str, email_address_str):
    validator = ErrorsCheck(phone_number_str=phone_number_str, email_address_str=email_address_str)
    errors = validator.output_errors()
    print(f"Проверка телефона: {phone_number_str}")
    print(f"Проверка email: {email_address_str}")
    print("-" * 20)
    print(errors)

# Пример использования
phone_number_str = "12345"  
email_address_str = "userexample.com"  

run_validation(phone_number_str, email_address_str)





    
