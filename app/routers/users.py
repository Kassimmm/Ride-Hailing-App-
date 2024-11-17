from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

import logging

logging.basicConfig(level=logging.INFO)
logging.info(f"TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID}")
logging.info(f"TWILIO_AUTH_TOKEN: {TWILIO_AUTH_TOKEN}")
logging.info(f"TWILIO_WHATSAPP_NUMBER: {TWILIO_WHATSAPP_NUMBER}")


router = APIRouter()
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserResponse)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    logging.info(f"Recipient phone number: whatsapp:{user.phone_number}")

    
    # Twilio WhatsApp verification
    message = twilio_client.messages.create(
        body="Welcome to the ride-hailing app! You've successfully signed up.",
        from_=TWILIO_WHATSAPP_NUMBER,  # Twilio sandbox number
        to=f"whatsapp:{user.phone_number}"
    )
    
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.UserResponse)
async def login(phone_number: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone_number=phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile/{user_id}", response_model=schemas.UserResponse)
async def edit_profile(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Edit a user's profile.

    Args:
        user_id (int): The ID of the user whose profile needs to be updated.
        updates (schemas.UserUpdate): The fields to update in the user's profile.
        db (Session): The database session.

    Returns:
        schemas.UserResponse: The updated user profile.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = crud.update_user(db, user_id=user_id, updates=updates)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user_id=user_id, updates=updates)

