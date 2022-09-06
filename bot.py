import time
import argparse

from orders.mirror_orders import *
from technical_analysis.moving_averages import *
from utils.log_utils import *


class TradingBot:
    def __init__(
            self,
            coin="BTC",
            stable_coin="USDT",
            budget=2000.0,
            gain_percentage=0.2,
            loss_percentage=0.05,
    ):
        self.coin = coin
        self.stable_coin = stable_coin
        self.budget = budget
        self.gain_percentage = gain_percentage
        self.loss_percentage = loss_percentage

    def run(self):
        coin = self.coin
        stable_coin = self.stable_coin
        market_pair = "{}/{}".format(coin, stable_coin)

        stable_coin_balance = self.budget
        coin_balance = 0.0

        sell_order = None

        incrementor = 0
        fixed_balance = stable_coin_balance / get_price_by_coin_pair(pair=market_pair)

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
            print("HODL BALANCE = {} USDT".format(fixed_balance*current_price))

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
                    plot=False
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
                        sell_order = open_sell_limit_order(
                            buy_price,
                            gain_percentage=self.gain_percentage,
                            loss_percentage=self.loss_percentage
                        )

                if not uptrend and momentum_down:
                    _, stable_coin_balance, coin_balance = sell_market(
                        coin_amount=coin_balance,
                        stable_coin_balance=stable_coin_balance,
                        coin_balance=coin_balance,
                        pair=market_pair
                    )

            time.sleep(3)
            incrementor += 1


if __name__ == '__main__':
    log_bot_version(version="Alpha 1.0.0")

    parser = argparse.ArgumentParser(description='Signarly TradingBot Command Line.')
    parser.add_argument(
        '--coin',
        default='BTC',
        help='Select the cryptocurrency you want to trade.'
    )
    parser.add_argument(
        '--stable-coin',
        default='USDT',
        help='Select the stable coin you want to trade against.'
    )
    parser.add_argument(
        '--budget',
        default=2000.0,
        help='Select the budget you want to start with.'
    )
    parser.add_argument(
        '--gain_percentage',
        default=0.2,
        help='Select the price percentage increase above which you want the bot to cash out.'
    )
    parser.add_argument(
        '--loss_percentage',
        default=0.05,
        help='Select the price percentage decrease below which you want the bot to cut losses.'
    )

    args = parser.parse_args()

    bot = TradingBot(
        coin=args.coin,
        stable_coin=args.stable_coin,
        budget=float(args.budget),
        gain_percentage=float(args.gain_percentage),
        loss_percentage=float(args.loss_percentage)
    )

    bot.run()
