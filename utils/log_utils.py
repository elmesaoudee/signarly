from datetime import datetime
from pyfiglet import Figlet


def log_bot_version(version="Alpha 1.0.0"):
    figlet = Figlet(font="slant")
    print(figlet.renderText("Signarly"))
    print("Version - {}".format(version))


def log_entry(coin, stable_coin, current_price, diff, coin_balance, stable_coin_balance):
    print("-----------------------------------------------")
    print("----            {} / {} TRADE          ----".format(coin, stable_coin))
    print("-----------------------------------------------")
    print("TIMESTAMP: {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    print("1 {} = {} {} {}".format(coin, current_price, stable_coin, diff))
    print("STABLE_COIN BALANCE = {} {}".format(str(stable_coin_balance), stable_coin))
    print("COIN BALANCE = {} {}".format(str(coin_balance), coin))
    print("TOTAL BALANCE = {} {}".format(str(stable_coin_balance + coin_balance * current_price), stable_coin))
    print("-----------------------------------------------")
