from technical_analysis import get_price_by_coin_pair


def buy_market(
        fiat_amount,
        fiat_balance,
        crypto_balance,
        pair="BNB/USDT"
):

    if fiat_amount >= fiat_balance and fiat_amount > 0 and fiat_balance > 0:
        buy_price = get_price_by_coin_pair(pair=pair)

        new_crypto_balance = crypto_balance + fiat_amount / buy_price
        new_fiat_balance = fiat_balance - fiat_amount

        print("BUY ORDER EXECUTED | Price: {}".format(buy_price))
        return buy_price, new_fiat_balance, new_crypto_balance

    else:
        print("BUY ORDER CANCELED: Insufficient fiat balance")
        return None, fiat_balance, crypto_balance


def sell_market(
        crypto_amount,
        fiat_balance,
        crypto_balance,
        pair="BNB/USDT"
):

    if crypto_amount <= crypto_balance and crypto_balance > 0 and crypto_amount > 0:
        sell_price = get_price_by_coin_pair(pair=pair)

        new_crypto_balance = crypto_balance - crypto_amount
        new_fiat_balance = fiat_balance + crypto_amount * sell_price

        print("SELL ORDER EXECUTED | Price: {}".format(sell_price))
        return sell_price, new_fiat_balance, new_crypto_balance
    else:
        print("SELL ORDER CANCELED: Insufficient crypto balance")
        return None, fiat_balance, crypto_balance


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
        fiat_balance,
        crypto_balance,
        pair="BNB/USDT"
):

    current_price = get_price_by_coin_pair(pair=pair)

    if current_price >= sell_limit_order['initial_buy_price'] * (1 + sell_limit_order['gain_percentage'] / 100) \
    or current_price <= sell_limit_order['initial_buy_price'] * (1 - sell_limit_order['loss_percentage'] / 100):
        print("SELL LIMIT ORDER EXECUTED")
        return None, sell_market(
            crypto_amount=crypto_balance,
            fiat_balance=fiat_balance,
            crypto_balance=crypto_balance,
            pair=pair
        )

    else:
        print("SELL LIMIT ORDER SKIPPED")
        return sell_limit_order, (None, fiat_balance, crypto_balance)