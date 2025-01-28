from fastapi import FastAPI
from app.users import router as router_users

app = FastAPI()


@app.get("/", tags=['Main'])
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_users)
