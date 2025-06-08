from dotenv import load_dotenv

load_dotenv()  # Automatically looks for a .env file in the current directory

from fastapi import FastAPI
from src.routes import agents
from src.routes import goals
from src.routes import user

app = FastAPI()

# Include route modules
app.include_router(agents.router)
app.include_router(goals.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Hello from Linguly!"}
