import re

from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo


class UserRegistration(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с +7 и содержать 10 цифр")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    re_password: str = Field(..., min_length=5, max_length=50, description="Повторите пароль")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+7\d{10}$', value):
            raise ValueError('Номер телефона должен начинаться с "+7" и содержать 10 цифр')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы один символ верхнего регистра')
        if not re.search(r'[$%&!:.]', v):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ ($%&!:)')
        if not re.match(r'^[a-zA-Z0-9$%&!:.]*$', v):
            raise ValueError('Пароль должен содержать только латинские буквы, цифры и специальные символы ($%&!:)')
        return v

    @field_validator("re_password")
    @classmethod
    def passwords_match(cls, values: str, info: ValidationInfo) -> str:
        if "re_password" in info.data and values != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return values

class CredentialUserAuth(BaseModel):
    user_credential: str = Field(..., description="Электронная почта или телефон пользователя")
    password: str

    def get_credential_type(self):
        if '@' in self.user_credential:
            return 'email'
        return 'phone_number'

    @field_validator("user_credential")
    @classmethod
    def validate_user_credential(cls, v):
        if "@" in v:
            assert len(v.split("@")) == 2, "Invalid email format."
        elif len(v) != 12:
            raise ValueError("Phone number must be 11 digits long.")
        return v
