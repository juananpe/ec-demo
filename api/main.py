import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from routes import admin, api

load_dotenv(".env")

app = FastAPI(title="Embedchain API")

app.include_router(api.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, log_level="info",
                reload=True, timeout_keep_alive=600)
