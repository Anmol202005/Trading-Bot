from fastapi import FastAPI
from pydantic import BaseModel
from bot.bot import BasicBot
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

bot = BasicBot(API_KEY, API_SECRET, testnet=True)

app = FastAPI(title="Binance Testnet Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    symbol: str
    side: str               
    qty: float
    price: float | None = None 
    slices: int | None = None    
    interval: int | None = None 

@app.post("/market")
def place_market(order: Order):
    """
    Place a market order
    """
    try:
        result = bot.market_order(order.symbol, order.side, order.qty)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/limit")
def place_limit(order: Order):
    """
    Place a limit order
    """
    if order.price is None:
        return {"status": "error", "message": "Price required for limit order"}
    try:
        result = bot.limit_order(order.symbol, order.side, order.qty, order.price)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/twap")
def place_twap(order: Order):
    """
    Place a TWAP order
    """
    if order.slices is None or order.interval is None:
        return {"status": "error", "message": "Slices and interval required for TWAP"}
    try:
        result = bot.twap_order(order.symbol, order.side, order.qty, order.slices, order.interval)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
