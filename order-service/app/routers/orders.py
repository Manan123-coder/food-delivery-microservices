from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from ..database import get_db
from ..models import Order
from ..schemas import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

USER_SERVICE = "http://user-service:8001"
RESTAURANT_SERVICE = "http://restaurant-service:8002"


# CREATE ORDER
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    # Check User Service
    try:
        user_response = requests.get(
            f"{USER_SERVICE}/users/{order.user_id}"
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="User Service unavailable"
        )

    if user_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check Restaurant Service
    try:
        menu_response = requests.get(
            f"{RESTAURANT_SERVICE}/restaurants/"
            f"{order.restaurant_id}/menu/"
            f"{order.menu_item_id}"
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Restaurant Service unavailable"
        )

    if menu_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    menu_item = menu_response.json()

    total_price = menu_item["price"] * order.quantity

    new_order = Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        menu_item_id=order.menu_item_id,
        quantity=order.quantity,
        total_price=total_price,
        status="PLACED"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


# READ ALL ORDERS
@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# READ ONE ORDER
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# UPDATE ORDER
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.quantity = order_data.quantity
    order.status = order_data.status

    # Get latest menu price
    try:
        menu_response = requests.get(
            f"{RESTAURANT_SERVICE}/restaurants/"
            f"{order.restaurant_id}/menu/"
            f"{order.menu_item_id}"
        )

        if menu_response.status_code == 200:
            menu_item = menu_response.json()
            order.total_price = (
                menu_item["price"] * order.quantity
            )

    except requests.RequestException:
        pass

    db.commit()
    db.refresh(order)

    return order


# DELETE ORDER
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }