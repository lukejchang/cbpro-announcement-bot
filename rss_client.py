from datetime import datetime
from typing import List

import dateutil.parser
import feedparser

from loggable import Loggable

COINBASE_FEED_URL = "https://blog.coinbase.com/feed"
ANNOUNCEMENT_SUFFIXES = ["is launching on Coinbase Pro", "are launching on Coinbase Pro"]
MAX_ANNOUNCEMENT_LAG_SECONDS = 99999999999999999999999999999999999


class SymbolFinder(Loggable):
    log_name = "SymbolFinder"

    def find_symbols(self) -> List[str]:
        self.log("Consuming Coinbase feed")
        feed = feedparser.parse(COINBASE_FEED_URL)
        if feed["bozo"] == 1:
            self.log(f"Feed is malformed: {feed}")

        items = feed["items"]
        symbols = []
        self.log(f"Parsing {len(items)} items")
        for item in items:
            title = item["title"]
            date = dateutil.parser.parse(item["date"]).astimezone()
            self.log(f"Parsing '{title}' from {date.date()} {date.time()}")

            item_symbols = self._find_symbols_from_title(title)
            filtered_symbols = [s for s in item_symbols if self._symbol_is_timely(s, date)]
            symbols += filtered_symbols

        return symbols

    @staticmethod
    def _find_symbols_from_title(title) -> List[str]:
        for suffix in ANNOUNCEMENT_SUFFIXES:
            suffix_idx = title.find(suffix)
            if suffix_idx == -1:
                continue

            symbols = []
            prefix = title[:suffix_idx]
            frags = prefix.split()

            for frag in frags:
                open_paren_idx = frag.find("(")
                if open_paren_idx == -1:
                    continue

                close_paren_idx = frag.find(")")
                symbol = frag[open_paren_idx + 1:close_paren_idx]
                symbols.append(symbol)

            return symbols

        return []

    def _symbol_is_timely(self, symbol, announcement_time: datetime) -> bool:
        lag = datetime.now().astimezone() - announcement_time.astimezone()
        if lag.seconds > MAX_ANNOUNCEMENT_LAG_SECONDS:
            self.log(f"Skipping {symbol} due to lag of {lag}")
            return False
        else:
            self.log(f"Found {symbol} with lag of {lag}")
            return True
