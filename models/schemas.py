from pydantic import BaseModel
from typing import Optional, List, Union


class CategoryOut(BaseModel):
    id: int
    name : str

    class Config:
        orm_mode = True


class ProductImage(BaseModel):
    id: int
    filename: str
    product_id : int

    class Config:
        orm_mode = True


class CreateProduct(BaseModel):
    name: str
    price: float
    category_id: int
    amount: int
    description : str

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: int
    name : str
    price : int
    category_id:int
    amount: int
    description: str
    images : List[ProductImage]
    category: CategoryOut

    class Config:
        orm_mode = True



class CreateCategory(BaseModel):
    name: str


    class Config:
        orm_mode = True


class CartItemOut(BaseModel):
    id : int
    quantity : int
    item : ProductOut

class WishlistItemOut(BaseModel):
    id : int
    quantity : int
    item : ProductOut


    