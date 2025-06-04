import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.db import sessionmanager
from app.routes.user import user_router

load_dotenv()

def init_app(init_db:bool = True):
    
    @asynccontextmanager
    async def lifespan(app:FastAPI) -> AsyncGenerator[None, None]:
        if init_db:
            url = os.getenv("DB_URL")
        
        if not url:
            raise RuntimeError("Missing Url env variable")
        
        print("server is starting")
    
        yield

        if init_db and sessionmanager._engine is not None:
            await sessionmanager.close()
            print("Server shutting down")

    server = FastAPI(lifespan=lifespan, title="Adult101")

    server.include_router(user_router, prefix='/auth', tags=['auth'])
    return server

app = init_app()
