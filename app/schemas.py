from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    name: str
    role: str
    phone_number: str
    emergency_contact: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    emergency_contact: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class RideRequest(BaseModel):
    current_location: str
    destination: str
    ride_type: str

class RideResponse(BaseModel):
    status: str
    driver_name: str
    car_model: str
    estimated_arrival: int
    fare_estimate: float

class RideUpdate(BaseModel):
    status: str
