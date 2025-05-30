from fastapi import APIRouter
from src.user.user_auth import UserAuth
from fastapi import HTTPException, status

user_auth = UserAuth()

router = APIRouter()


@router.get("/user")
def read_user():
    return {"message": "You are user1(test)"}

@router.post("/user/login")
def login(email: str, password: str):
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login data"
        )
    try:
        return user_auth.login(email=email, password=password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/user/signup")
def signup(name: str, email: str, password: str):
    if not name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signup data"
        )
    try:
        return user_auth.signup(name=name, email=email, password=password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
