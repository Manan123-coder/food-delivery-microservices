from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    location: str


class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str | None
    price: float

    class Config:
        from_attributes = True