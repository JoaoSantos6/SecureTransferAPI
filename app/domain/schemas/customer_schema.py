from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class CustomerBase(BaseModel):
    id: int
    full_name: str
    birthday: date
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class CustomerPrivate(CustomerBase):
    cpf: str
    email: EmailStr
    phone_number: str
    balance: float
    currency: str
    account_number: str

class CustomerPublic(CustomerBase):
    pass