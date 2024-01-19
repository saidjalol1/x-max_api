from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session, joinedload
from utils import verify_api_key
from config import get_db
from models.models import *

from typing import List, Annotated

from models.schemas import CreateProduct, ProductOut


products = APIRouter(
    prefix="/products",
    tags=["products",]
)


@products.post("/add")
async def create_product(
    name: Annotated[str, Form(...)],
    price: Annotated[int, Form(...)],
    category_id: Annotated[int, Form(...)],
    amount: Annotated[int, Form(...)],
    description: Annotated[str, Form(...)],
    images: List[UploadFile] = File(...),
    api_key : str = Depends(verify_api_key),
    db: Session = Depends(get_db),
    ):

    db_product = Product(
        name = name,
        price = price,
        category_id = category_id,
        amount= amount,
        description = description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    for i in images:
        with open(f"product_images/{i.filename}", "wb") as image_file:
            image_file.write(await i.read())
        db_image = ProductImage(filename = i.filename, product_id=db_product.id)
        db.add(db_image)

        db.commit()
        db.refresh(db_image)

    return {"messages": "Seccessfully Created"}


@products.get("/all_products", response_model=List[ProductOut])
async def fetch_all(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    products = db.query(Product).options(joinedload(Product.images)).all()
    return products


@products.patch("/update_products/{id}")
async def fetch_product(
    id : int,
    name: Annotated[str, Form()] | None = None,
    price: Annotated[int, Form()] | None = None,
    category_id: Annotated[int, Form()] | None = None,
    amount: Annotated[int, Form(...)] | None = None,
    description: Annotated[str, Form()] | None = None,
    api_key : str = Depends(verify_api_key),
    db: Session = Depends(get_db)
    ):
    product = db.query(Product).filter_by(id=id).first()
    if name:
        product.name = name
    if price:
        product.price = price
    if category_id:
        product.category_id = category_id
    if amount:
        product.amount = amount
    if description:
        product.description = description
    

    db.add(product)
    db.commit()
    db.refresh(product)
    return {"messages": "Successfully updated"} 


@products.delete("/delete/{id}")
async def delete_product(
    id : int,
    api_key: str = Depends(verify_api_key),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter_by(id=id).delete()
    db.commit()
    return {"messages":"Deleted successfully"}

