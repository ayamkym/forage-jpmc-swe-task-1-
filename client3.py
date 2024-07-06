import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# Number of server requests
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote.get('stock', 'N/A')
    bid_price = float(quote['top_bid']['price']) if 'top_bid' in quote else None
    ask_price = float(quote['top_ask']['price']) if 'top_ask' in quote else None
    if bid_price is not None and ask_price is not None:
        price = (bid_price + ask_price) / 2
    else:
        price = bid_price if bid_price is not None else ask_price
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None
    return price_a / price_b

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        stock_prices = {}
        
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            stock_prices[stock] = price
            print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")

        stocks = list(stock_prices.keys())
        if len(stocks) >= 2:
            ratio = getRatio(stock_prices[stocks[0]], stock_prices[stocks[1]])
            print(f"Ratio of {stocks[0]} to {stocks[1]}: {ratio}")
