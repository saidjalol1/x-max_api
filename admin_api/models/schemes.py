from pydantic import BaseModel
from typing import Optional, List, Union

class UserIn(BaseModel):
    username : str
    email : Optional(str)
    password : str
    is_superuser : Optional(bool)
    is_seller : Optional(bool)
    is_cashier : Optional(bool)