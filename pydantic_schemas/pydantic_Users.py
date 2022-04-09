from pydantic import BaseModel, EmailStr
class base_user(BaseModel):
    email : EmailStr
    password : str
    class Config:
        orm_mode = True

class in_user(base_user):
    name: str
    class Config:
        orm_mode = True

class final_user(in_user):
    id : int    
    class Config:
        orm_mode = True
