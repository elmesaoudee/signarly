import ccxt
import time
import random

from constants import BINANCE_API_KEY, BINANCE_API_SECRET

exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
    'enableRateLimit': True,
})

symbol = 'BTC/ETH'
type = 'limit'  # or 'market'
side = 'sell'  # or 'buy'
amount = 1.0
price = 0.060154  # or None

# extra params and overrides if needed
params = {
    'test': True,  # test if it's valid, but don't actually place it
}

for i in range(50):
    if (exchange.has['fetchTicker']):
        print(exchange.fetch_ticker('BNB/UlSDT')['info']['lastPrice']) # ticker for LTC/ZEC
    time.sleep(3)