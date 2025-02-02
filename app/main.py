from datetime import datetime

from fastapi import FastAPI

from app.database import db_create_tables
from app.users.router import router as users_router
from app.product.router import router as product_router

db_create_tables()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await db_create_tables()


@app.get("/", tags=['Main'])
def home_page():
    return {"message": "Привет!"}


app.include_router(users_router)
app.include_router(product_router)
