from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils import verify_api_key, get_or_create_user_token
from config import get_db
from models import models


main_routes = APIRouter(
    prefix="/main",
    tags=["main_routes",],
)


@main_routes.get("/")
async def index():
    return {"messages":"type '/' to get api documentation"}

@main_routes.get("/cart")
async def cart_page(
    api_key: str = Depends(verify_api_key),
    token: str = Depends(get_or_create_user_token),
    db : Session = Depends(get_db)
    ):
    carts = db.query(models.CartItem).filter_by(token=token).all()
    return carts