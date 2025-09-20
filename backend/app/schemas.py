from pydantic import BaseModel
from typing import Optional

# Pydantic models for data validation and serialization

# Schema for user registration
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

# Schema for user login
class UserLogin(BaseModel):
    email: str
    password: str

# Schema for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Base schema for a sweet
class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    description: str
    image_url: Optional[str] = None

# Schema for a sweet response, including the ID
class SweetResponse(SweetBase):
    id: int
    class Config:
        orm_mode = True

# Schema for a user response
class User(BaseModel):
    email: str
    name: Optional[str] = None
    role: str
