from fastapi import APIRouter, HTTPException, Depends

from models.models import Category
from models.schemas import CreateCategory, CategoryOut
from models.models import *

from sqlalchemy.orm import Session
from typing import List

from config import get_db
from utils import verify_api_key



route = APIRouter(
    prefix="/category",
    tags=["category routes",]
)


@route.post("/add", response_model= CategoryOut)
async def create_category(
    category : CreateCategory,
    api_key: str = Depends(verify_api_key),
    db : Session = Depends(get_db),
    ):
    category = Category(**category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    category = {
        "category": category
    }
    return category
    

@route.get("/all_categories",response_model=List[CategoryOut])
async def fetch_all(
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
    ):
    categories = db.query(Category).all()
    return categories


@route.patch("/update/{id}")
async def update_category(
    id: int,
    name : str,
    api_key : str = Depends(verify_api_key),
    db : Session = Depends(get_db)
    ):
    category = db.query(Category).filter(Category.id == id).first()
    category.name = name
    db.commit()
    db.refresh(category)
    category = {
        "category": category
    }
    return category


@route.delete("/delete/{id}")
async def delete_category(
    id: int,
    api_key: str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    category = db.query(Category).filter_by(id=id).delete()
    db.commit()
    return {"message":"Deleted successfully"}