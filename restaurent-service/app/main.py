from fastapi import FastAPI

from .database import Base, engine
from .routers import restaurants


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Food Delivery - Restaurant Service",
    description="Manages restaurants and menu items.",
    version="1.0.0"
)


app.include_router(restaurants.router)


@app.get("/")
def home():
    return {
        "message": "Food Delivery Restaurant Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }