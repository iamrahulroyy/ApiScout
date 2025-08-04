from fastapi import FastAPI
from contextlib import asynccontextmanager

import uvicorn
from app.db.database import init_db
from app.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="ApiScout - LLM-Powered API Tester",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host= "localhost", port=8009)