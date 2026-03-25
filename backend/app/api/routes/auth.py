from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(payload: AuthRequest) -> dict:
    return {"message": "User registered", "email": payload.email}


@router.post("/login")
def login(payload: AuthRequest) -> dict:
    return {"access_token": "mock-jwt-token", "token_type": "bearer"}
