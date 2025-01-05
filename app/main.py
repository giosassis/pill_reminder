# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine, get_db_connection
from app.routes import medicines, send_email
import uvicorn

app = FastAPI()

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Montando arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluindo os routers
app.include_router(medicines.router)
app.include_router(send_email.router)  # Agora estamos incluindo o router correto

# Rota inicial
@app.get("/")
def read_root():
    print("Server is running")
    return {"message": "welcome to my personal application"}

if __name__ == '__main__':
    get_db_connection()
    uvicorn.run(app, host="127.0.0.1", port=8000)
