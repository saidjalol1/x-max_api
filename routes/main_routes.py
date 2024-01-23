from fastapi import APIRouter, HTTPException, Depends, Query
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
    id: Optional[int] = None,
    name: Optional[str] = None,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    query = db.query(models.Product).options(joinedload(models.Product.category)).options(joinedload(models.Product.images))

    if name:
        query = query.filter(models.Product.name.contains(name))
    if id:
        try:
            query = query.filter(models.Product.category_id == id)
        except Exception as e:
            query = "Mahsulot lar mavjud emas"
            
    products = query.all()
    categories = db.query(models.Category).all()

    response = {
        "products": products,
        "categories": categories
    }

    return response

