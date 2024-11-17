from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, rides

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(rides.router)
