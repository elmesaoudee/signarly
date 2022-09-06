import ccxt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.constants import OHLCV_COLS


class BinanceAPICallException(Exception):
    pass


class IndicatorNotFoundException(Exception):
    pass


exchange = ccxt.binance()


def get_price_by_coin_pair(pair: str = "BTC/USDT") -> float:

    try:
        if exchange.has['fetchTicker']:
            return float(exchange.fetch_ticker(pair.upper())['info']['lastPrice'])
    except Exception as e:
        raise BinanceAPICallException(e)


def fetch_olhcv_candles_dataframe(
        symol="BNB/USDT",
        timeframe="5m",
        limit=50,
        emas=None
) -> pd.DataFrame:

    candles = exchange.fetch_ohlcv(symbol=symol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(candles, columns=OHLCV_COLS)
    df['timestamp'] = df['timestamp'].values.astype(dtype='datetime64[ms]')

    if emas is not None:
        for ema in emas:
            if ema <= limit:
                df['ema' + str(ema)] = df['closed'].ewm(span=ema, adjust=False).mean()

    return df


def get_current_ema_values(candles: pd.DataFrame, emas: list) -> list:

    ema_values = []
    current_ohlcv = candles.iloc[-1]
    for ema in emas:
        indicator_name = 'ema' + str(ema)
        if indicator_name not in candles.columns:
            raise IndicatorNotFoundException
        ema_values.append(current_ohlcv[indicator_name])

    return ema_values


def get_series_orientation(series: pd.Series, plot=False) -> (float, list):

    diffs = np.diff(series)
    gradients = np.sign(diffs)
    orientation = gradients.mean()

    if plot:
        series.plot()
        plt.show()

    return orientation, gradients


def is_indicator_on_uptrend(
        candles: pd.DataFrame,
        emas: list,
        steps: int = 5,
        trend_threshold: float = 0.1,
        plot=True
) -> bool:

    uptrends = []
    for ema in emas:
        if ema <= candles.shape[0]:
            indicator_name = 'ema' + str(ema)

            if indicator_name not in candles.columns:
                raise IndicatorNotFoundException

            indicator_series = candles[indicator_name][-steps:]
            orientation, _ = get_series_orientation(indicator_series, plot=plot)

            uptrend = orientation >= trend_threshold
            uptrends.append(uptrend)

    return sum(uptrends) > len(uptrends) / 2


def is_ema_picking_momentum(candles: pd.DataFrame, emas: list) -> bool:

    current_ema_values = get_current_ema_values(candles, emas=emas)
    smallest_ema = current_ema_values[0]
    rest_emas = current_ema_values[1:]

    uptrend = True
    for ema in rest_emas:
        uptrend &= smallest_ema >= ema

    return uptrend


def is_ema_losing_momentum(candles: pd.DataFrame, emas: list) -> bool:

    current_ema_values = get_current_ema_values(candles, emas=emas)
    smallest_ema = current_ema_values[0]
    rest_emas = current_ema_values[1:]

    for ema in rest_emas:
        if smallest_ema < ema:
            return True

    return False
