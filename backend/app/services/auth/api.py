from sqlmodel import Session, select
from app.database import engine
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
from app.database import engine
# from app.services.rooms.models import Room

from fastapi import APIRouter
from fastapi import HTTPException, status

from dotenv import load_dotenv
import os
load_dotenv()

from app.services.auth.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your own values from the Google Developer Console
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google"
router = APIRouter()

### AUTHENTICATION ROUTES ###
### ROOT IS /auth ###

from fastapi.responses import JSONResponse, RedirectResponse

@router.get("/login/google")
async def login_google():
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return RedirectResponse(url=google_auth_url)

@router.get("/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == user_info.json()["email"])).first()
        if not user:
          session.add(User(**user_info.json()))
          session.commit()

    # Generate a JWT token for the user
    token = jwt.encode({"sub": user_info.json()["email"]}, GOOGLE_CLIENT_SECRET, algorithm="HS256")

    # Create a response with the token set in a cookie
    response = RedirectResponse(url="http://localhost:3000/settings")
    response.set_cookie(key="session_token", value=token, samesite="Lax")

    return response

@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])