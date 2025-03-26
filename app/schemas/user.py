
from pydantic import BaseModel, EmailStr, Field, constr
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
        allow_population_by_field_name = True 

class UserInResponse(UserBase):
    uid: str

    class Config:
        json_encoders = {
            UUID: str
        }

class UserCreate(UserBase):
    pass