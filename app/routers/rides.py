from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book", response_model=schemas.RideResponse)
async def book_ride(user_id: int, ride_details: schemas.RideRequest, db: Session = Depends(get_db)):
    """
    Book a ride for a user.

    Args:
        user_id (int): The ID of the user booking the ride.
        ride_details (schemas.RideCreate): Details of the ride being booked.
        db (Session): The database session.

    Returns:
        schemas.RideResponse: Details of the booked ride.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_ride(db, ride=ride_details, user_id=user_id)


@router.put("/ride/{ride_id}/status", response_model=schemas.RideResponse)
async def update_ride_status(ride_id: int, status_update: schemas.RideUpdate, db: Session = Depends(get_db)):
    db_ride = crud.get_ride(db, ride_id=ride_id)
    if not db_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return crud.update_ride_status(db, ride_id=ride_id, status=status_update.status)
