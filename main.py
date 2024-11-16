from fastapi import FastAPI

from database.db_config import db_config, close

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db_config()

@app.on_event("shutdown")
async def shutdown():
    await close()
@app.get("/")
async def root():
    return {"message": "Hello World"}
