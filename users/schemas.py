from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class SUserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
#    re_password: str = Field(..., min_length=5, max_length=50, description="Повторите пароль")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value
