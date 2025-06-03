from src.db_proxy.db_proxy import get_db
from argon2 import PasswordHasher
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.user.types import UserInfo

# Secret key & algorithm
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000

# Tell FastAPI where tokens will come from (Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class UserAuth:
    """
    UserAuth class handles user authentication operations such as login and signup.
    """

    def __init__(self):
        self.user_db = get_db("user")
        # Create a hasher with default parameters (good defaults)
        self.ph = PasswordHasher()

    def login(self, email: str, password: str):
        # Validate the input data
        if not email or not password:
            raise ValueError("Invalid login data: email and password are required")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")

        users = self.user_db.find("user_auth", {"email": email})
        if not users:
            raise ValueError("User not found")
        user = users[0]

        # Verify against the hashed password
        try:
            self.ph.verify(user["password"], password)
        except Exception as e:
            raise ValueError("Invalid password") from e

        # Generate and return jwt token
        token = self.create_access_token(
            data={"sub": str(user["_id"]), "email": email, "name": user["name"]}
        )
        return {"access_token": token, "token_type": "bearer"}

    def signup(self, name: str, email: str, password: str):
        # Validate the input data
        # Check if email is unique, valid, and password meets security requirements
        if not name or not email or not password:
            raise ValueError(
                "Invalid signup data: name, email, and password are required"
            )
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")
        # Check if the email already exists
        existing_users = self.user_db.find("user_auth", {"email": email})
        if existing_users:
            raise ValueError("Email already exists")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Everything is valid, let's prepare to create the user
        hashed_password = self.ph.hash(password)
        # Create the user in the database
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
        }
        user_id = self.user_db.insert("user_auth", user_data)

        token = self.create_access_token(
            data={"sub": str(user_id), "email": email, "name": name}
        )
        return {"access_token": token, "token_type": "bearer"}

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependency to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInfo:
    """Validates the JWT token and returns the user data."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return UserInfo(
            sub=user_id, email=payload.get("email"), name=payload.get("name")
        )
    except JWTError:
        raise credentials_exception


def validate_token(token: str = Depends(oauth2_scheme)):
    """This is used when the user data is not needed, just the token validation."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
