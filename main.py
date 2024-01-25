from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from routes import main_routes, product_routes, category_routes, category_routes, cart_routes, wishlist, authentication_routes

from config import engine, get_db
from utils import SECRET_KEY
from fastapi.staticfiles import StaticFiles

from models import models

models.Base.metadata.create_all(bind=engine)
get_db()



app = FastAPI()

# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount("/images", StaticFiles(directory="product_images/"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.include_router(main_routes.main_routes)
app.include_router(product_routes.products)
app.include_router(category_routes.route)
app.include_router(cart_routes.route)
app.include_router(wishlist.route)
app.include_router(authentication_routes.route)


@app.get("/")
async def index():
    return {"messages": "type '/doc' to get the API docs"}