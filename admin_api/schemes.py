from pydantic import BaseModel
from typing import Optional, List, Union

class SuperUserAuth(BaseModel):
    username : str
    email : str
    password : str
    is_superuser : bool

class SuperUserOut(BaseModel):
    id : int
    username : str
    email : str 
    is_superuser : bool

