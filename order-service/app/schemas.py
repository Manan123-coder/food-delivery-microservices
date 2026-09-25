from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    menu_item_id: int
    quantity: int = Field(gt=0)


class OrderUpdate(BaseModel):
    quantity: int = Field(gt=0)
    status: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    menu_item_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True