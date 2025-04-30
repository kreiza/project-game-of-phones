import re

class ValidationError(ValueError):
    pass

class Validator:
    def __init__(self, value):
        self.value = value

    def validate(self):
        raise NotImplementedError("класи повинні реалізувати цей метод")

class PhoneNumberValidator(Validator):
    MIN_DIGIT_LEN = 7
    MAX_DIGIT_LEN = 15
    ALLOWED_CHARS_PATTERN = re.compile(r"^[+\d\s()/-]*$")

    def validate(self):
        if not self.value:
            raise ValidationError("Номер телефону не надано або він порожній.")

        if not isinstance(self.value, str):
            raise ValidationError("Помилка формату: Номер телефону має бути рядком (string).")

        if not self.ALLOWED_CHARS_PATTERN.match(self.value):
             raise ValidationError("Ви використали неприпустимий символ у номері телефону.")

        if '+' in self.value and self.value.find('+') != 0:
            raise ValidationError("Символ '+' дозволено лише на початку номера.")

        digits_only = ''.join(filter(str.isdigit, self.value))

        if not digits_only:
             raise ValidationError("У номері телефону мають бути цифри.")

        if len(digits_only) < self.MIN_DIGIT_LEN:
            raise ValidationError(f"Номер телефону надто короткий (мінімум {self.MIN_DIGIT_LEN} цифр).")

        if len(digits_only) > self.MAX_DIGIT_LEN:
            raise ValidationError(f"Номер телефону надто довгий (максимум {self.MAX_DIGIT_LEN} цифр).")

class EmailValidator(Validator):
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def validate(self):
        if not self.value:
            raise ValidationError("Email адреса не надана або вона порожня.")

        if not isinstance(self.value, str):
            raise ValidationError("Помилка формату: Email має бути рядком (string).")

        if not self.EMAIL_PATTERN.match(self.value):
            if '@' not in self.value:
                 raise ValidationError("Email адреса повинна містити символ '@'.")
            if self.value.count('@') > 1:
                 raise ValidationError("Email адреса повинна містити рівно один символ '@'.")
            if '.' not in self.value.split('@', 1)[-1]:
                 raise ValidationError("Частина домену (після '@') повинна містити крапку '.'." )
            raise ValidationError("Email адреса має невірний формат.")

def run_validation_with_exceptions(phone_str, email_str):
    print(f"Перевірка телефону: '{phone_str}'")
    try:
        phone_validator = PhoneNumberValidator(phone_str)
        phone_validator.validate()
        print("  Статус: OK")
    except ValidationError as e:
        print(f"  Статус: Помилка -> {e}")

    print("-" * 20)

    print(f"Перевірка email: '{email_str}'")
    try:
        email_validator = EmailValidator(email_str)
        email_validator.validate()
        print("  Статус: OK")
    except ValidationError as e:
        print(f"  Статус: Помилка -> {e}")

    print("=" * 30 + "\n")


print("Приклад:")
run_validation_with_exceptions("12345", "userexample.com")





    
