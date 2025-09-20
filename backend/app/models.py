from sqlalchemy import Column, Integer, String, Float
from .database import Base

# Define the User model for the database table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False) # Hashed password
    name = Column(String)
    role = Column(String, default="user") # 'user' or 'admin'

# Define the Sweet model for the database table
class Sweet(Base):
    __tablename__ = "sweets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    description = Column(String)
    image_url = Column(String)