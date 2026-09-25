from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Restaurant, MenuItem
from ..schemas import (
    RestaurantCreate,
    RestaurantResponse,
    MenuItemCreate,
    MenuItemResponse
)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


# =========================
# RESTAURANT CRUD
# =========================

# CREATE RESTAURANT
@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    new_restaurant = Restaurant(
        name=restaurant.name,
        location=restaurant.location
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


# READ ALL RESTAURANTS
@router.get("/", response_model=list[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


# READ ONE RESTAURANT
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant


# UPDATE RESTAURANT
@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    restaurant.name = restaurant_data.name
    restaurant.location = restaurant_data.location

    db.commit()
    db.refresh(restaurant)

    return restaurant


# DELETE RESTAURANT
@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    # Delete menu items belonging to this restaurant first
    db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id
    ).delete()

    db.delete(restaurant)
    db.commit()

    return {
        "message": "Restaurant deleted successfully"
    }


# =========================
# MENU ITEM CRUD
# =========================

# CREATE MENU ITEM
@router.post(
    "/{restaurant_id}/menu",
    response_model=MenuItemResponse
)
def create_menu_item(
    restaurant_id: int,
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    new_item = MenuItem(
        restaurant_id=restaurant_id,
        name=item.name,
        description=item.description,
        price=item.price
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# READ ALL MENU ITEMS
@router.get(
    "/{restaurant_id}/menu",
    response_model=list[MenuItemResponse]
)
def get_menu(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .all()
    )


# READ ONE MENU ITEM
@router.get(
    "/{restaurant_id}/menu/{item_id}",
    response_model=MenuItemResponse
)
def get_menu_item(
    restaurant_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(MenuItem)
        .filter(
            MenuItem.id == item_id,
            MenuItem.restaurant_id == restaurant_id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return item


# UPDATE MENU ITEM
@router.put(
    "/{restaurant_id}/menu/{item_id}",
    response_model=MenuItemResponse
)
def update_menu_item(
    restaurant_id: int,
    item_id: int,
    item_data: MenuItemCreate,
    db: Session = Depends(get_db)
):
    item = (
        db.query(MenuItem)
        .filter(
            MenuItem.id == item_id,
            MenuItem.restaurant_id == restaurant_id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    item.name = item_data.name
    item.description = item_data.description
    item.price = item_data.price

    db.commit()
    db.refresh(item)

    return item


# DELETE MENU ITEM
@router.delete(
    "/{restaurant_id}/menu/{item_id}"
)
def delete_menu_item(
    restaurant_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(MenuItem)
        .filter(
            MenuItem.id == item_id,
            MenuItem.restaurant_id == restaurant_id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }