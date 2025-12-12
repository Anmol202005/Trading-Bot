import time
import hmac
import hashlib
import requests
import urllib.parse


class BinanceFuturesClient:

    def __init__(self, api_key: str, api_secret: str, base_url: str, logger=None):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.logger = logger

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query = urllib.parse.urlencode(params)
        signature = hmac.new(self.api_secret, query.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params: dict):
        url = self.base_url + path
        signed = self._sign(params)

        if self.logger:
            self.logger.info(f"REQUEST {method} {url} PARAMS={params}")

        try:
            res = self.session.request(method, url, params=signed)
            res.raise_for_status()

            if self.logger:
                self.logger.info(f"RESPONSE {res.status_code}: {res.text}")

            return res.json()

        except Exception as e:
            if self.logger:
                self.logger.error(f"ERROR: {str(e)}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, tif="GTC"):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = tif

        if order_type == "STOP":
            params["stopPrice"] = stop_price
            params["price"] = price
            params["timeInForce"] = tif

        return self._request("POST", "/fapi/v1/order", params)
