from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine, get_db_connection
from app.routes import medicines, send_email
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(medicines.router)
app.include_router(send_email.router) 

@app.get("/")
def read_root():
    print("Server is running")
    return {"message": "Welcome to my personal backend application!"}
