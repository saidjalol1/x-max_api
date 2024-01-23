from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from utils import verify_api_key, get_or_create_user_token
from config import get_db
from models import models, schemas

from typing import List, Optional


main_routes = APIRouter(
    prefix="/home",
    tags=["main_routes",],
)



@main_routes.get("/")
async def index(
    name: Optional[str],
    api_key : str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    if name == None:
        products = db.query(models.Product).options(joinedload(models.Product.category)).options(joinedload(models.Product.images)).all()
        categories = db.query(models.Category).all()
    else:
        products = db.query(models.Product).options(joinedload(models.Product.category)).options(joinedload(models.Product.images)).filter(models.Category)
    respons = {
        "products": products,
        "categories": categories
    }
    return respons

