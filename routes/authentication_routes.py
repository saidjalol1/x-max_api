from fastapi import APIRouter, Depends, Body, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from typing import List


route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")





# @route.post("/login")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return {"token":"token"}


# def fake_decode_user(token):
#     return User(username=token)


# def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
#     user = fake_decode_user(token)
#     return user


# @route.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user