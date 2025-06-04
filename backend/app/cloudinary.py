import asyncio
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import UploadFile
load_dotenv()


# Configuration       
cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

async def upload(file:UploadFile):
    file.file.seek(0)
    loop = asyncio.get_event_loop()
    upload_result = await loop.run_in_executor(None, lambda:cloudinary.uploader.upload(file))
    return {"secure_url":upload_result["secure_url"], 'url':upload_result["url"]}