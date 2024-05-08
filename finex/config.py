from fastapi import FastAPI, APIRouter
from routers import candle, ticker

app = FastAPI()

app.include_router(candle.router, tags=['Candle'])
