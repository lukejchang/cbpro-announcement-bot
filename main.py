import time

from cbpro_client import CbProClient
from loggable import Loggable
from rss_client import SymbolFinder

BUY_LIMIT_MULTIPLIER = 1.2
ORDER_SIZE_USD = 1000
SLEEP_SECONDS = 60


def run_bot():
    logger = Loggable()
    logger.log_name = "Main"

    rss = SymbolFinder()
    cbpro = CbProClient()

    while True:
        symbols = rss.find_symbols()
        for symbol in symbols:
            last_price = cbpro.get_last_price(symbol)
            limit = last_price * BUY_LIMIT_MULTIPLIER
            size = ORDER_SIZE_USD / limit
            cbpro.buy(symbol, limit, size)

        logger.log(f"Sleeping for {SLEEP_SECONDS} seconds")
        time.sleep(SLEEP_SECONDS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
