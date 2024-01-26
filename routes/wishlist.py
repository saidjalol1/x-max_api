from fastapi import APIRouter, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session, joinedload

from utils import verify_api_key, get_or_create_user_token
from config import get_db

from models.models import WishlistItem, Category, Product
from models.schemas import WishlistItemOut, WhishlistItemIn

from typing import List, Optional


route = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"]
)

@route.get("/")
async def wishlist(
    api_key: str = Depends(verify_api_key),
    user_token: str = Depends(get_or_create_user_token),
    db : Session = Depends(get_db)
):
    cart = db.query(WishlistItem).options(joinedload(WishlistItem.item).joinedload(Product.images)).filter(WishlistItem.token==user_token).all()
    cart_objects = {
        "whishlist_item": cart
    }
    return cart_objects


@route.post("/wishlist_toggle/")    
async def add_to_wishlist(
    whishlist_item : WhishlistItemIn,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
        existing_whishlist_item = db.query(WishlistItem).filter(
            WishlistItem.token == user_token, WishlistItem.item_id == whishlist_item.item_id
        ).first()

        if existing_whishlist_item:
            db.delete(existing_whishlist_item)
            db.commit()
            return {"wishlist_item": "Removed from Wishlist"}
        else:
            new_item = WishlistItem(
                token = user_token,
                item_id = whishlist_item.item_id,
                )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"cart_item" : new_item,
                    "message": "Added to Wishlist"
                    }

