import uvicorn
from app.database import get_db_connection
from app.main import app

if __name__ == '__main__':
    get_db_connection()  # Inicializa a conexão com o banco
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
