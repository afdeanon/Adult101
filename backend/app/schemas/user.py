from pydantic import BaseModel

class GoogleAuthToken(BaseModel):
    id_token:str


class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    user_id:str | None = None


class UserSignUp(BaseModel):
    email:str
    password:str | None = None

class UserAdditionalFields(BaseModel):
    username:str
    bio:str | None = None
    profile_pic:str | None = None