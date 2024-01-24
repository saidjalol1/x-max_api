from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session, joinedload

from utils import verify_api_key, get_or_create_user_token
from config import get_db

from models.models import WishlistItem, Category, Product
from models.schemas import WishlistItemOut

from typing import List, Optional


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
    cart = db.query(WishlistItem).options(joinedload(WishlistItem.item)).filter(WishlistItem.token==user_token, WishlistItem.quantity > 0).all()
    return cart


@route.post("/add_to_whishlist/{product_id}")
async def add_to_cart(
    id : int,
    user_token : str =Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
        try:
            cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.item_id == id).first()
            cart_item.quantity += 1
            db.commit()
            cart_item = {
                "item": cart_item
            }
            return cart_item
        except Exception as e:
            new_item = WishlistItem(
                token = user_token,
                quantity = 1,
                item_id = id,
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            item = {
                "item": new_item
            }
            return item


@route.post("/remove_from_whishlist/{product_id}")
async def remove_from_cart(
    id : int,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.item_id == id).first()
        cart_item.quantity -= 1
        db.commit()
        if cart_item.quantity == 0:
            db.delete(cart_item)
            return {"message":"Product Deleted successfully"}
        return {"messages":"Product removed from the whishlist successfully!!!"}
    except Exception as e:
        return {"message": "Product is not exists in whishlist!!!"}

    

@route.delete("/delete/{id}")
async def delete_cart_item(
    id : int,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.id == id).first()
        db.delete(cart_item)
        db.commit()
        return {"messages":"Product deleted from the whishlist successfully!!!"}
    except Exception as e:
        return {"message": "Product is not exists in whishlist!!!"}




