import os
import secrets
from dotenv import load_dotenv
from fastapi import Header, Depends, HTTPException, Request, Response


load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


# Api Retrieve and Verification functions 
def get_api_key(api_key: str = Header(...)):
    return api_key

def verify_api_key(api_key: str = Depends(get_api_key)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
    


def generate_token_for_user():
    token = secrets.token_hex(16)
    return token


def get_or_create_user_token(request:Request, response: Response = None):
    user_token = request.session.get("user_token")

    if user_token is None:
        token = generate_token_for_user()
        request.session["user_token"] = token

    return user_token
    
