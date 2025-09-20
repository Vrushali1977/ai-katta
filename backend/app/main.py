import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, sweets
from .database import engine, Base

# Initialize the FastAPI app with a title for documentation
app = FastAPI(title="AI-Katta Sweet Shop API")

# Configure CORS to allow communication from the frontend
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for different functionalities
app.include_router(users.router, prefix="/api/auth", tags=["Auth"])
app.include_router(sweets.router, prefix="/api/sweets", tags=["Sweets"])

# Create database tables based on the models defined
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the AI-Katta Sweet Shop API"}
