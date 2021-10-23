import time

from orders.mirror_orders import *
from technical_analysis.moving_averages import *
from utils.log_utils import *


class TradingBot:
    def __init__(self, coin="BTC", stable_coin="USDT"):
        self.coin = coin
        self.stable_coin = stable_coin

    def run(self):
        coin = self.coin
        stable_coin = self.stable_coin
        market_pair = "{}/{}".format(coin, stable_coin)

        stable_coin_balance = 2000.0
        coin_balance = 0.0

        sell_order = None

        incrementor = 0

        while True:
            if incrementor == 18:
                incrementor = 0

            current_price = get_price_by_coin_pair(pair=market_pair)
            if sell_order is not None:
                diff = " | SELL LIMIT ORDER DIFF: ({}%)".format(
                    str(round((current_price - sell_order['initial_buy_price'])/sell_order['initial_buy_price']*100, 2))
                )
            else:
                diff = ""

            log_entry(
                coin=coin,
                stable_coin=stable_coin,
                current_price=current_price,
                diff=diff,
                coin_balance=coin_balance,
                stable_coin_balance=stable_coin_balance
            )

            if sell_order is not None:
                print("CHECKING SELL LIMIT ORDER")
                sell_order, sell_output = sell_limit_order(
                    sell_order,
                    stable_coin_balance,
                    coin_balance,
                    pair=market_pair
                )

                if sell_order is None:
                    time.sleep(30)

                sell_price, stable_coin_balance, coin_balance = sell_output

            if incrementor % 18 == 0:
                candle_sticks = fetch_olhcv_candles_dataframe(
                    symol="BNB/USDT",
                    timeframe="3m",
                    limit=50,
                    emas=[7, 20, 50]
                )

                uptrend = is_indicator_on_uptrend(
                    candle_sticks,
                    emas=[7, 20, 50],
                    steps=5,
                    plot=True
                )

                momentum_up = is_ema_picking_momentum(
                    candle_sticks,
                    emas=[7, 20, 50]
                )

                momentum_down = is_ema_losing_momentum(
                    candle_sticks,
                    emas=[7, 20, 50]
                )

                if uptrend and momentum_up:
                    buy_price, stable_coin_balance, coin_balance = buy_market(
                        stable_coin_amount=stable_coin_balance,
                        stable_coin_balance=stable_coin_balance,
                        coin_balance=coin_balance,
                        pair=market_pair
                    )
                    if sell_order is None and buy_price is not None:
                        sell_order = open_sell_limit_order(buy_price, gain_percentage=0.3, loss_percentage=0.05)

                if not uptrend and momentum_down:
                    _, stable_coin_balance, coin_balance = sell_market(
                        coin_amount=coin_balance,
                        stable_coin_balance=stable_coin_balance,
                        coin_balance=coin_balance,
                        pair=market_pair
                    )

            time.sleep(10)
            incrementor += 1


if __name__ == '__main__':
    log_bot_version(version="Alpha 1.0.0")

    bot = TradingBot(
        coin="BNB",
        stable_coin="USDT"
    )

    bot.run()
