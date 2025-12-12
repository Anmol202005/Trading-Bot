from binance.client import Client
import time

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """
        api_key: Binance API key
        api_secret: Binance API secret
        testnet: True → use Binance Futures Testnet
        """
        self.client = Client(api_key, api_secret, testnet=testnet)

    def market_order(self, symbol, side, quantity):
        return self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

    def limit_order(self, symbol, side, quantity, price):
        return self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

    def stop_limit_order(self, symbol, side, quantity, price, stop_price):
        return self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            stopPrice=stop_price,
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )

    def twap_order(self, symbol, side, total_qty, slices, duration):
        interval = duration / slices
        qty_per_slice = total_qty / slices
        results = []
        for _ in range(slices):
            res = self.market_order(symbol, side, qty_per_slice)
            results.append(res)
            time.sleep(interval)
        return results
