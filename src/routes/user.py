from fastapi import APIRouter, HTTPException, status, Depends
from src.user.user_auth import UserAuth
from src.user.types import LoginRequest, SignupRequest, Token, TokenData

user_auth = UserAuth()
router = APIRouter()


@router.get("/user/me")
def read_user(current_user: TokenData = Depends(user_auth.get_current_user)):
    return {
        "message": f"Hello, {current_user.name}! You are logged in as {current_user.email}.",
        "current_user": current_user,
    }


@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    try:
        return user_auth.login(**request.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/signup", response_model=Token)
def signup(request: SignupRequest):
    try:
        return user_auth.signup(**request.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
