from fastapi import FastAPI

from .database import Base, engine
from .routers import orders


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Food Delivery - Order Service",
    description="Creates and manages food delivery orders.",
    version="1.0.0"
)


app.include_router(orders.router)


@app.get("/")
def home():

    return {
        "message": "Food Delivery Order Service is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }