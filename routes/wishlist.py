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
    cart = db.query(WishlistItem).options(joinedload(WishlistItem.item).joinedload(Product.images)).filter(WishlistItem.token==user_token, WishlistItem.quantity > 0).all()
    cart_objects = {
        "whishlist_item": cart
    }
    return cart_objects


@route.post("/add_to_wishlist/")    
async def add_to_wishlist(
    whishlist_item : WhishlistItemIn,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        existing_whishlist_item = db.query(WishlistItem).filter(
            WishlistItem.token == user_token, WishlistItem.item_id == whishlist_item.item_id
        ).first()

        if existing_whishlist_item:
            existing_whishlist_item.quantity += whishlist_item.quantity
            db.commit()
            db.refresh(existing_whishlist_item)
            return {"cart_item": existing_whishlist_item}
        else:
            new_item = WhishlistItemIn(
                token = user_token,
                quantity = whishlist_item.quantity,
                item_id = whishlist_item.item_id,
                )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"cart_item" : new_item}
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during the operation.",
        )


@route.post("/remove_from_wishlist/")
async def remove_from_cart(
    wishlist_item : WhishlistItemIn,
    user_token : str = Depends(get_or_create_user_token),
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    try:
        cart_item = db.query(WishlistItem).filter(WishlistItem.token == user_token, WishlistItem.item_id == wishlist_item.item_id).first()
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




