from pydantic import BaseModel
from typing import Optional
from typing import List

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
    price : int
    category_id:int
    amount: int
    description: str
    images : List[ProductImage]

    class Config:
        orm_mode = True



class CreateCategory(BaseModel):
    name: str


    class Config:
        orm_mode = True