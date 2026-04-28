from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

# Demo credentials (replace with DB lookup in production)
DEMO_USERS = {
    "admin@acme.com": {"password": "demo1234", "name": "Rafael Costa", "role": "admin"},
    "user@acme.com": {"password": "demo1234", "name": "Ana Lima", "role": "user"},
}


class LoginRequest(BaseModel):
    email: str
    password: str


def create_token(email: str, role: str) -> str:
    payload = {
        "sub": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token inválido")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return decode_token(credentials.credentials)


@router.post("/login")
async def login(body: LoginRequest):
    user = DEMO_USERS.get(body.email)
    if not user or user["password"] != body.password:
        raise HTTPException(401, "Credenciais inválidas")

    token = create_token(body.email, user["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": body.email, "name": user["name"], "role": user["role"]},
    }


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
