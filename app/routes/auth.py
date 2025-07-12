from fastapi import APIRouter, Request
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

router = APIRouter()

# Environment variables
client_id = os.getenv("API_KEY")
client_secret = os.getenv("SECRET_KEY")
redirect_uri = os.getenv("REDIRECT_URL")
state = os.getenv("STATE")


# ✅ OAuth Login URL (only if needed)
@router.get("/login")
def login():
    login_url = (
        f"https://api.upstox.com/v2/login/authorization/dialog?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}"
    )
    return {"login_url": login_url}


# ✅ Exchange Code for Access Token (dynamic)
@router.post("/get-access-token")
async def get_access_token(request: Request):
    body = await request.json()
    code = body.get("code")

    if not code:
        return {"error": "Missing 'code' in request body"}

    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }

    response = requests.post(url, headers=headers, data=data)

    return {
        "status": response.status_code,
        "data": response.json()
    }
