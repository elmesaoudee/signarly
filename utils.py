def ema(steps, price):
    k = 2 / (steps + 1)
    return price * k + ema(steps-1, price) * (1-k)