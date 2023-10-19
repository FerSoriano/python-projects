from fastapi import FastAPI
from routers import users

app = FastAPI()

app.include_router(users.router)

@app.get('/')
async def saludo():
    return "Hola, bienvenido a la API"


