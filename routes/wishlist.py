from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session, joinedload

from utils import verify_api_key, get_or_create_user_token
from config import get_db

from models.models import WishlistItem, Category, Product
from models.schemas import WishlistItemOut

from typing import List


route = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"]
)

@route.get("/", response_model=List[WishlistItemOut])
async def wishlist(
    api_key: str = Depends(verify_api_key),
    user_token: str = Depends(get_or_create_user_token),
    db : Session = Depends(get_db)
):
    cart = db.query(WishlistItem).options(joinedload(WishlistItem.item)).filter(WishlistItem.token==user_token).all()
    cart_items = {
        "items": cart
    }
    return cart_items


@route.post("/add_to_cart/{id}")
async def add_to_cart(
    id : int,
    quantity : int,
    user_token : str =Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.id == id).first()
        cart_item.quantity += quantity
        db.commit()
    except Exception as e:
        new_item = WishlistItem(
            token = user_token,
            quantity = quantity,
            item_id = id,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

    return {"messages":"Product added to the cart successfully!!!"}


@route.post("/remove_from_cart/{id}")
async def remove_from_cart(
    id : int,
    quantity : int,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.id == id).first()
    if cart_item:
        cart_item.quantity -= quantity
        db.commit()
    elif cart_item.quantity == 0:
        cart_item.delete()
        db.commit()
    else:
        pass
    return {"messages":"Product removed from the cart successfully!!!"}
    




