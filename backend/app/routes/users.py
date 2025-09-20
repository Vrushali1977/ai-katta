from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserLogin, Token, User as UserSchema
from ..models import User as UserModel
from ..database import get_db
from ..auth import authenticate_user, create_access_token, get_current_user
from ..utils import get_password_hash
from datetime import timedelta

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    # Check if a user with the same email already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password for security
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(email=user.email, password=hashed_password, name=user.name)
    
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": f"User {new_user.email} registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint to log in a user and return a JWT access token.
    """
    user_data = authenticate_user(db, user.email, user.password)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create an access token that expires in 30 minutes
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
