from fastapi import APIRouter, Depends,Body, Form, Request, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import  RedirectResponse



from .admin_utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from .schemes import SuperUserAuth, SuperUserOut

from config import get_db
from sqlalchemy.orm import Session
from models import models



route = APIRouter(
    prefix="/admin",
    tags=["Admin authorizations"]
)



@route.post("/signup", response_model=SuperUserOut)
async def signup(data: SuperUserAuth, db : Session = Depends(get_db)):
    user =  db.query(models.User).filter_by(email=data.email).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Akaxon Bu email bilan Ro'yxatdan O'tilbopti lekin"
        )
    user = models.User(
        username=data.username,
        email=data.email,
        password=get_hashed_password(data.password),
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@route.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username = form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username"
        )
    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }
