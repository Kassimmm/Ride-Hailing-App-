from sqlalchemy.orm import Session
from . import models, schemas
import random

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from sqlalchemy.orm import Session
from app.models import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone(db: Session, phone_number: str):
    # Ensure phone_number is always a string
    return db.query(models.User).filter(models.User.phone_number == str(phone_number)).first()


def update_user(db: Session, user_id: int, updates: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Ride CRUD
def create_ride(db: Session, ride: schemas.RideRequest, user_id: int):
    db_ride = models.Ride(
        user_id=user_id,
        current_location=ride.current_location,
        destination=ride.destination,
        ride_type=ride.ride_type,
        status="Pending",
        driver_name=f"Driver {random.choice(['Alice', 'Bob', 'Charlie'])}",
        car_model=f"{random.choice(['Toyota Corolla', 'Honda Civic'])}",
        estimated_arrival=random.randint(5, 15),
        fare_estimate=round(random.uniform(10, 50), 2)
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_ride(db: Session, ride_id: int):
    return db.query(models.Ride).filter(models.Ride.id == ride_id).first()

def update_ride_status(db: Session, ride_id: int, status: str):
    db_ride = get_ride(db, ride_id)
    db_ride.status = status
    db.commit()
    db.refresh(db_ride)
    return db_ride
