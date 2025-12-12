import argparse
import os
from bot.client import BinanceFuturesClient
from bot.bot import BasicBot
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger("TradingBot")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("bot.log")
fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(fh)


API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BASE_URL = "https://testnet.binancefuture.com"


def get_args():
    p = argparse.ArgumentParser()

    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True, choices=["BUY", "SELL"])
    p.add_argument("--type", required=True,
                   choices=["MARKET", "LIMIT", "STOP_LIMIT", "TWAP"])

    p.add_argument("--quantity", type=float, required=True)
    p.add_argument("--price", type=float)
    p.add_argument("--stop-price", type=float)

    p.add_argument("--slices", type=int)
    p.add_argument("--duration", type=int)

    return p.parse_args()


def main():
    args = get_args()

    client = BinanceFuturesClient(API_KEY, API_SECRET, BASE_URL, logger)
    bot = BasicBot(client)

    if args.type == "MARKET":
        resp = bot.place_market(args.symbol, args.side, args.quantity)

    elif args.type == "LIMIT":
        if args.price is None:
            print("LIMIT requires --price")
            return
        resp = bot.place_limit(args.symbol, args.side, args.quantity, args.price)

    elif args.type == "STOP_LIMIT":
        if args.price is None or args.stop_price is None:
            print("STOP_LIMIT requires --price and --stop-price")
            return
        resp = bot.place_stop_limit(
            args.symbol, args.side, args.quantity, args.price, args.stop_price
        )

    elif args.type == "TWAP":
        resp = bot.twap(
            args.symbol,
            args.side,
            args.quantity,
            args.slices or 5,
            args.duration or 60
        )

    print("\n--- ORDER RESULT ---")
    print(resp)


if __name__ == "__main__":
    main()
