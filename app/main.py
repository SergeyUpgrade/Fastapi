from fastapi import FastAPI
from app.users.router import router as users_router
from app.product.router import router as product_router

app = FastAPI()


@app.get("/", tags=['Main'])
def home_page():
    return {"message": "Привет!"}


app.include_router(users_router)
app.include_router(product_router)
