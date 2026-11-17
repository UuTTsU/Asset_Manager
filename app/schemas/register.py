from datetime import date
from typing_extensions import Self
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator, ConfigDict


class RegisterSchema(BaseModel):
    name: str = Field(min_length=1,max_length=30)
    last_name: str= Field(min_length=1,max_length=20)
    email: EmailStr
    password: str = Field(min_length=8,max_length=255)
    repeat_password: str = Field(min_length=8,max_length=255)
    birthday: date

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.repeat_password:
            raise ValueError('Passwords do not match')
        return self
    @field_validator('password')
    @classmethod
    def check_passwords_have_numbers(cls, v: str) -> str :
        has_digits = any(char.isdigit() for char in v)
        if not has_digits:
            raise ValueError('Passwords do not have numbers')
        return v


class RegisterResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    last_name: str
    email: EmailStr

