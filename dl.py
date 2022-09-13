# -> standard
import json
import glob
from os import listdir, remove
from datetime import datetime
from os.path import isfile, join
from typing import Any
# -> third party
import pandas as pd
import requests_cache
import yfinance as yf


def get_all_symbols() -> list[str]:
    with open('symbols.lst', 'r') as symbols:
        return symbols.read().split()


def calculate_loss(prices: pd.DataFrame) -> tuple[int, float]:
    last_price: float = prices["Close"][-1]
    last_date = prices.index[-1]
    highest_loss: tuple[float, Any] = (9999999999999999, 0)

    for date_c, row in prices[::-1].iterrows():
        if (last_price / row["Close"] - 1) < highest_loss[0]:
            highest_loss = ((last_price / row["Close"] - 1), date_c)

    delta: int = highest_loss[1] - last_date

    return (abs(delta.days), highest_loss[0] * 100)


def main():

    # -> Symbols to update
    for f in stock_jsons:
        current_symbol: str = f.split("_")[1].split(".json")[0]
        last_update = datetime.strptime(f.split("_")[0], '%Y-%m-%d').date()
        if today < last_update:
            old_symbols.append(current_symbol)

    s = set(old_symbols)
    symbols = [x for x in get_all_symbols() if x not in s]

    for sym in symbols:
        latest = datetime.today().strftime('%Y-%m-%d')

        for f in glob.glob(f"data/*_{sym}.json"):
            if latest not in f:
                print(f"-- Removing old: {f}")
                remove(f)

        print(f"++ Adding {sym}")
        format_datatable: dict[str, list[list[str | int | float]]] = {
            "data": []
        }

        data = yf.Tickers(sym)
        full_name: str = data.tickers[sym].info["longName"]
        hist = pd.DataFrame(data.tickers[sym].history(period="1y"))
        hist.index = pd.to_datetime(hist.index)

        days, loss = calculate_loss(hist)

        stonk: dict[str, str | float] = {
            "name": full_name,
            "symbol": sym,
            "latest": latest,
            "days": days,
            "loss": loss,
        }

        with open(f"data/{latest}_{sym}.json", 'w') as name:
            name.write(json.dumps(stonk))

        jsonfiles = [f for f in listdir("data") if isfile(
            join("data", f)) and ".json" in f]
        for file in jsonfiles:
            with open(f"data/{file}", 'r') as data:
                x = json.loads(data.read())
                format_datatable["data"].append(
                    [x["name"], x["symbol"], x["days"], x["loss"], x["latest"]])

        with open("all.json", 'w') as all:
            all.write(json.dumps(format_datatable))

        format_datatable["data"] = []


if __name__ == "__main__":
    session = requests_cache.CachedSession("yfinance.cache")
    session.headers[
        "User-agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0"
    old_symbols: list[str] = []

    today = datetime.now().date()
    stock_jsons = [f for f in listdir("data") if isfile(
        join("data", f)) and ".json" in f]

    main()