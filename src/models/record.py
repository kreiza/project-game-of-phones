from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class Contact(BaseModel):
    """
    Pydantic model for a phonebook record.
    """

    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    phone_number: PhoneNumber
    address: str = Field(..., max_length=255)
    email: EmailStr
    birthday: date
    contact_note: Optional[str] = Field(None, max_length=500)

    @field_validator("birthday")
    def validate_birthday(cls, value: date) -> date:
        """
        Validates that the birthday is not in the future.
        """
        if value > date.today():
            raise ValueError("Birthday cannot be in the future.")
        return value
