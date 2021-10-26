import cbpro

from loggable import Loggable

SANDBOX_KEY = "INSERT_KEY_HERE"
SANDBOX_SECRET = "INSERT_SECRET_HERE"
SANDBOX_PASSPHRASE = "INSERT_PASSPHRASE_HERE"
SANDBOX_URL = "https://api-public.sandbox.pro.coinbase.com"


class CbProClient(Loggable):
    log_name = "CbPro"

    def __init__(self):
        self.log("Initializing public client")
        self.public_client = cbpro.PublicClient()
        self.log(f"Initializing sandbox client with key {SANDBOX_KEY}")
        self.sandbox_client = cbpro.AuthenticatedClient(
            SANDBOX_KEY,
            SANDBOX_SECRET,
            SANDBOX_PASSPHRASE,
            api_url=SANDBOX_URL,
        )

    def get_last_price(self, symbol: str) -> float:
        product_id = self._product_id(symbol)
        self.log(f"Getting last ticker for {product_id}")
        try:
            ticker = self.public_client.get_product_ticker(product_id)
            self.log(f"Last ticker for {product_id}: {ticker}")
            return float(ticker["price"])
        except Exception as e:
            self.log(f"get_product_ticker exception: {e}")

    def buy(self, symbol: str, limit: float, size: float) -> None:
        product_id = self._product_id(symbol)
        try:
            self.log(f"Placing limit buy for {product_id}, limit {limit}, size {size}")
            order_details = self.sandbox_client.place_limit_order(product_id, "buy", limit, size)
            self.log(f"Placed order: {order_details}")
        except Exception as e:
            self.log(f"place_limit_order exception: {e}")

    @staticmethod
    def _product_id(symbol):
        return symbol + "-USD"
