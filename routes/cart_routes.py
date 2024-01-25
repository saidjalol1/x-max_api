from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session, joinedload

from utils import verify_api_key, get_or_create_user_token
from config import get_db

from models.models import CartItem, Category, Product
from models.schemas import CartItemOut

from typing import List


route = APIRouter(
    prefix="/cart",
    tags=["Cart routes"]
)

@route.get("/")
async def cart_page(
    api_key: str = Depends(verify_api_key),
    user_token: str = Depends(get_or_create_user_token),
    db : Session = Depends(get_db)
):
    cart = db.query(CartItem).options(joinedload(CartItem.item)).filter(CartItem.token==user_token, CartItem.quantity > 0).all()
    cart_objects = {
        "cart_objects": cart
    }
    return cart_objects


@route.post("/add_to_cart/{id}")
async def add_to_cart(
    id : int,
    user_token : str =Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(CartItem).filter(CartItem.token == user_token, CartItem.item_id == id).first()
        cart_item.quantity += 1
        db.commit()
        cart_item = {
            "cart_item": cart_item
        }
        return cart_item
    except Exception as e:
        new_item = CartItem(
            token = user_token,
            quantity = 1,
            item_id = id,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        item = {
            "item" : new_item
        }
        return item

    


@route.post("/remove_from_cart/{id}")
async def remove_from_cart(
    id : int,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(CartItem).filter(CartItem.token == user_token, CartItem.item_id == id).first()
        cart_item.quantity -= 1
        db.commit()
        if cart_item.quantity == 0:
            db.delete(cart_item)
            return {"message":"Product Deleted successfully"}
        return {"messages":"Product removed from the cart successfully!!!"}
    except Exception as e:
        return {"message": "Product is not exists in cart!!!"}
    

@route.delete("/delete/{id}")
async def delete_cart_item(
    id : int,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(CartItem).filter(CartItem.token == user_token, CartItem.id == id).first()
        db.delete(cart_item)
        db.commit()
        return {"messages":"Product deleted from the cart successfully!!!"}
    except Exception as e:
        return {"message": "Product is not exists in cart!!!"}




