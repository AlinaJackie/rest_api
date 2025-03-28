from fastapi import FastAPI
from routes import router

app = FastAPI(title="Library API")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Library API!"}
