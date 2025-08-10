# routers/external.py
from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/external")
async def fetch_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com")
    return response.json()
