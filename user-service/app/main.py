from fastapi import FastAPI

from .database import Base, engine
from .routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery - User Service"
)

app.include_router(users.router)


@app.get("/")
def home():
    return {
        "message": "Food Delivery User Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }