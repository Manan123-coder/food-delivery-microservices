from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        nullable=False
    )

    menu_item_id = Column(
        Integer,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="PLACED"
    )