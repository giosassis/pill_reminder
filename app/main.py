from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routes import medications, send_email, email_history

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(medications.router)
app.include_router(send_email.router) 
app.include_router(email_history.router) 

@app.get("/")
def read_root():
    print("Server is running")
    return {"message": "Welcome to my personal backend application!"}
