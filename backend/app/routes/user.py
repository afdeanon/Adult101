import os
from typing import Annotated
import httpx
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from app.cloudinary import upload
from app.db import get_db
from app.schemas.user import GoogleAuthToken, Token, TokenData, UserAdditionalFields, UserSignUp
from app.services.user import UserService
from app.utils.jwt import jwt_service

load_dotenv()
user_router = APIRouter()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
user_service = UserService()

@user_router.post('/google')
async def google_auth(token:GoogleAuthToken):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token.id_token}")

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID token")
    
    data = response.json()

    if data['aud'] != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid client ID")
    
    email = data['email']
    name = data['name']

    access_token = await jwt_service.create_token(TokenData(user_id=email))

    return {"access_token":access_token, "token_type":"bearer"}



@user_router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:AsyncSession = Depends(get_db)):
    email = await user_service.authenticate(form_data.username, form_data.password, db)

    access_token = await jwt_service.create_token(TokenData(user_id=email))

    return {"access_token":access_token, "token_type":"bearer"}

@user_router.post("/signup")
async def signup(user:UserSignUp, db:AsyncSession = Depends(get_db)):
    if not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing password")
    await user_service.signUp(user, db)

    access_token = await jwt_service.create_token(TokenData(user_id=user.email))
    return {"access_token":access_token, "token_type":"bearer"}

@user_router.post("/signup-google")
async def signup(user = Depends(user_service.get_user)):
    await user_service.signUp(UserSignUp(email=user))

    access_token = jwt_service.create_token(TokenData(user_id=user))

    return {"access_token":access_token, "token_type":"bearer"}
@user_router.post("/additionalFields")
async def add_additional_fields(data:UserAdditionalFields, db:AsyncSession = Depends(get_db)):
    await user_service.completeUserSignUp(data, db)
        

@user_router.post("/profilepic")
async def update_profilepic(picture:UploadFile = File(...), user:str = Depends(user_service.get_user), db:AsyncSession = Depends(get_db)):
    urls = await upload(picture)
    await user_service.updateProfilePicture(urls['source_url'])
