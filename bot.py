import time

from orders import buy_market, sell_market, open_sell_limit_order, sell_limit_order
from technical_analysis import fetch_olhcv_candles_dataframe, is_indicator_on_uptrend, is_ema_picking_momentum, \
    is_ema_losing_momentum, get_price_by_coin_pair


def run():
    COIN = "BNB"
    CURRENCY = "USDT"
    MARKET_PAIR = "{}/{}".format(COIN, CURRENCY)

    FIAT_BALANCE = 2000.0
    CRYPTO_BALANCE = 0.0

    SELL_ORDER = None

    INCREMENTOR = 0


    while True:
        if INCREMENTOR == 12: INCREMENTOR = 0


        current_price = get_price_by_coin_pair(pair=MARKET_PAIR)
        print("-----------------------------------------------")
        print("1 {} = {} {}".format(COIN, current_price, CURRENCY))
        print("FIAT BALANCE = {} {}".format(str(FIAT_BALANCE), CURRENCY))
        print("CRYPTO BALANCE = {} {}".format(str(CRYPTO_BALANCE), COIN))
        print("TOTAL BALANCE = {} {}".format(str(FIAT_BALANCE + CRYPTO_BALANCE * current_price), CURRENCY))
        print("-----------------------------------------------")

        if SELL_ORDER is not None:
            print("CHECKING SELL LIMIT ORDER")
            SELL_ORDER, sell_output = sell_limit_order(
                SELL_ORDER,
                FIAT_BALANCE,
                CRYPTO_BALANCE,
                pair=MARKET_PAIR
            )

            if SELL_ORDER is None:
                time.sleep(30)

            sell_price, FIAT_BALANCE, CRYPTO_BALANCE = sell_output

        if INCREMENTOR % 6 == 0:
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
                buy_price, FIAT_BALANCE, CRYPTO_BALANCE = buy_market(
                    fiat_amount=FIAT_BALANCE,
                    fiat_balance=FIAT_BALANCE,
                    crypto_balance=CRYPTO_BALANCE,
                    pair=MARKET_PAIR
                )
                if SELL_ORDER is None and buy_price is not None:
                    SELL_ORDER = open_sell_limit_order(buy_price, gain_percentage=0.3, loss_percentage=0.05)

            if not uptrend and momentum_down:
                _, FIAT_BALANCE, CRYPTO_BALANCE = sell_market(
                    crypto_amount=CRYPTO_BALANCE,
                    fiat_balance=FIAT_BALANCE,
                    crypto_balance=CRYPTO_BALANCE,
                    pair=MARKET_PAIR
                )

        time.sleep(30)
        INCREMENTOR += 1


if __name__ == '__main__':
    run()
