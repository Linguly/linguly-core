from fastapi import APIRouter, HTTPException, status
from src.user.user_auth import UserAuth
from src.user.types import LoginRequest, SignupRequest

user_auth = UserAuth()
router = APIRouter()

@router.get("/user")
def read_user():
    return {"message": "You are user1(test)"}

@router.post("/user/login")
def login(request: LoginRequest):
    try:
        return user_auth.login(**request.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/user/signup")
def signup(request: SignupRequest):
    try:
        return user_auth.signup(**request.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
