from technical_analysis.moving_averages import get_price_by_coin_pair


def buy_market(
        stable_coin_amount,
        stable_coin_balance,
        coin_balance,
        pair="BNB/USDT"
):

    if stable_coin_amount >= stable_coin_balance and stable_coin_amount > 0 and stable_coin_balance > 0:
        buy_price = get_price_by_coin_pair(pair=pair)

        new_crypto_balance = coin_balance + stable_coin_amount / buy_price
        new_fiat_balance = stable_coin_balance - stable_coin_amount

        print("BUY ORDER EXECUTED | Price: {}".format(buy_price))
        return buy_price, new_fiat_balance, new_crypto_balance

    else:
        print("BUY ORDER CANCELED: Insufficient fiat balance")
        return None, stable_coin_balance, coin_balance


def sell_market(
        coin_amount,
        stable_coin_balance,
        coin_balance,
        pair="BNB/USDT"
):

    if coin_amount <= coin_balance and coin_balance > 0 and coin_amount > 0:
        sell_price = get_price_by_coin_pair(pair=pair)

        new_crypto_balance = coin_balance - coin_amount
        new_fiat_balance = stable_coin_balance + coin_amount * sell_price

        print("SELL ORDER EXECUTED | Price: {}".format(sell_price))
        return sell_price, new_fiat_balance, new_crypto_balance
    else:
        print("SELL ORDER CANCELED: Insufficient crypto balance")
        return None, stable_coin_balance, coin_balance


def open_sell_limit_order(initial_buy_price, gain_percentage, loss_percentage):
    print("LIMIT ORDER SET | Price: {} | Gain: {}% | Loss: {}%".format(
        initial_buy_price, gain_percentage, loss_percentage
    ))

    return {
            "initial_buy_price": initial_buy_price,
            "gain_percentage": gain_percentage,
            "loss_percentage": loss_percentage
        }


def close_sell_limit_order():
    return None


def sell_limit_order(
        sell_limit_order,
        stable_coin_balance,
        coin_balance,
        pair="BNB/USDT"
):

    current_price = get_price_by_coin_pair(pair=pair)

    if current_price >= sell_limit_order['initial_buy_price'] * (1 + sell_limit_order['gain_percentage'] / 100) \
    or current_price <= sell_limit_order['initial_buy_price'] * (1 - sell_limit_order['loss_percentage'] / 100):
        print("SELL LIMIT ORDER EXECUTED")
        return None, sell_market(
            coin_amount=coin_balance,
            stable_coin_balance=stable_coin_balance,
            coin_balance=coin_balance,
            pair=pair
        )

    else:
        print("SELL LIMIT ORDER SKIPPED")
        return sell_limit_order, (None, stable_coin_balance, coin_balance)