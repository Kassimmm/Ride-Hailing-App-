from sqlalchemy import Column, Integer, String, ForeignKey, Float
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    phone_number = Column(String, unique=True, index=True)
    emergency_contact = Column(String)

class Ride(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    current_location = Column(String)
    destination = Column(String)
    ride_type = Column(String)
    status = Column(String, default="Pending")
    driver_name = Column(String)
    car_model = Column(String)
    estimated_arrival = Column(Integer)
    fare_estimate = Column(Float)
