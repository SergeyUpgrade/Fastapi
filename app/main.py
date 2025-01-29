from fastapi import FastAPI
from app.users.router import router

app = FastAPI()


@app.get("/", tags=['Main'])
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router)
