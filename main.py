from fastapi import FastAPI

from database.db_config import db_config, close
from routers.admin_endpoints import admin_router
from routers.auth_endpoints import auth_router
from routers.solicitacao_endpoints import solicitacao_router

app = FastAPI()
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(solicitacao_router)
@app.on_event("startup")
async def startup():
    await db_config()

@app.on_event("shutdown")
async def shutdown():
    await close()
@app.get("/")
async def root():
    return {"message": "Hello World"}
