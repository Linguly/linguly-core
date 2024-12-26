from fastapi import FastAPI
from src.routes import agent_proxy
from src.routes import user

app = FastAPI()

# Include route modules
app.include_router(agent_proxy.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Hello from Linguly!"}