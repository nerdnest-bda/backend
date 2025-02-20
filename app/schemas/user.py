
from pydantic import BaseModel, EmailStr, constr
from uuid import UUID


class UserBase(BaseModel):
    uid: str
    full_name: str
    email: EmailStr
    password: constr(min_length=6)
    gpa: float
    verbal_score: int
    quant_score: int
    awa_score: float

    class Config:

        json_encoders = {
            UUID: str
        }

class UserInResponse(UserBase):
    _id: str

    class Config:
        json_encoders = {
            UUID: str
        }

class UserCreate(UserBase):
    pass