from pydantic import BaseModel

class UserBase(BaseModel):
   email: str
   name: str
      
class UserCreate(UserBase):
   password: str

class User(UserBase):
   is_active: bool
   id: int
   
   class Config:
      orm_mode = True  