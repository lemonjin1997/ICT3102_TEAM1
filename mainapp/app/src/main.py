from fastapi import FastAPI
from src.routes.user import user

app = FastAPI()
app.include_router(user)