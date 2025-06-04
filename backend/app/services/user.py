import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserAdditionalFields, UserSignUp
from app.utils.jwt import jwt_service
from app.utils.security import hash_pwd, oauth2_scheme, verify_pwd



class UserService:
    async def authenticate(email:str, password:str, db:AsyncSession):
        stmt = select(User.password).where(User.email == email)
        try:
            res = await db.execute(stmt)
            hashed_password = res.scalar_one()
            
            if not verify_pwd(password, hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password or email")
            
            return email
        except Exception:
            raise
    
    async def get_user(token:str = Depends(oauth2_scheme)):
        #Depends(oauth2_scheme) parses "Bearer " part out and just returns the token
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt_service.parse_token(token)
            user_id = payload.get('user_id')
            if not user_id:
                raise credentials_exception
            return user_id
        except jwt.exceptions:
            raise credentials_exception
    
    async def signUp(user:UserSignUp, db:AsyncSession):
        new_user = user.model_dump()
        if new_user['password']:
            new_user['password'] = hash_pwd(new_user['password'])
        user_instance = User(**new_user)

        db.add(user_instance)
        await db.commit()
    

    async def completeUserSignUp(additional_fields:UserAdditionalFields, user:str, db:AsyncSession):
        user = select(User).where(User.email == user)

        for attr, value in additional_fields.model_dump():
            if value:
                setattr(user,attr, value)
        db.commit()
