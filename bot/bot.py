from binance.client import Client
import time
import logging

logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger = logging.getLogger()
        self.logger.info("Initialized BasicBot with testnet=%s", testnet)

    def _serialize_response(self, res):
        return {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in res.items()}

    def market_order(self, symbol, side, quantity):
        self.logger.info("Placing MARKET order: symbol=%s, side=%s, qty=%s", symbol, side, quantity)
        try:
            res = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            serialized = self._serialize_response(res)
            self.logger.info("MARKET order response: %s", serialized)
            return {"status": "success", "response": serialized}
        except Exception as e:
            self.logger.error("Error placing MARKET order: %s", e)
            return {"status": "error", "message": str(e)}

    def limit_order(self, symbol, side, quantity, price):
        self.logger.info("Placing LIMIT order: symbol=%s, side=%s, qty=%s, price=%s", symbol, side, quantity, price)
        try:
            res = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price
            )
            serialized = self._serialize_response(res)
            self.logger.info("LIMIT order response: %s", serialized)
            return {"status": "success", "response": serialized}
        except Exception as e:
            self.logger.error("Error placing LIMIT order: %s", e)
            return {"status": "error", "message": str(e)}

    def stop_limit_order(self, symbol, side, quantity, price, stop_price):
        self.logger.info("Placing STOP-LIMIT order: symbol=%s, side=%s, qty=%s, price=%s, stop_price=%s",
                         symbol, side, quantity, price, stop_price)
        try:
            res = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                stopPrice=stop_price,
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )
            serialized = self._serialize_response(res)
            self.logger.info("STOP-LIMIT order response: %s", serialized)
            return {"status": "success", "response": serialized}
        except Exception as e:
            self.logger.error("Error placing STOP-LIMIT order: %s", e)
            return {"status": "error", "message": str(e)}

    def twap_order(self, symbol, side, total_qty, slices, duration):
        interval = duration / slices
        qty_per_slice = total_qty / slices
        self.logger.info("Starting TWAP: symbol=%s, side=%s, total_qty=%s, slices=%s, interval=%s",
                         symbol, side, total_qty, slices, interval)
        results = []
        for i in range(slices):
            res = self.market_order(symbol, side, qty_per_slice)
            results.append(res)
            self.logger.info("TWAP slice %d executed: %s", i + 1, res)
            time.sleep(interval)
        self.logger.info("TWAP order completed for %s slices", slices)
        return results
