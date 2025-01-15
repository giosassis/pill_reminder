from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str

    class Config:
        orm_mode = True