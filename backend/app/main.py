import asyncio
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import sessionmanager
from app.routes.user import user_router

load_dotenv()
origins = [
    "http://localhost",
    "http://localhost:8081",
]

def init_app(init_db:bool = True):
    
    url = os.getenv("DB_URL")
    if init_db:
        sessionmanager.init(url)
        # asyncio.run(sessionmanager.create_tables())
        loop = asyncio.get_event_loop()
        loop.create_task(sessionmanager.create_tables())
    
    if not url:
        raise RuntimeError("Missing Url env variable")
    
    @asynccontextmanager
    async def lifespan(app:FastAPI) -> AsyncGenerator[None, None]:
        print("server is starting")
    
        yield

        if init_db and sessionmanager._engine is not None:
            await sessionmanager.close()
            print("Server shutting down")

    server = FastAPI(lifespan=lifespan, title="Adult101")
    server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows requests from these origins
    allow_credentials=True,      # Allows cookies, authorization headers etc.
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],         # Allows all headers
    )
    server.include_router(user_router, prefix='/auth', tags=['auth'])
    return server

app = init_app()
