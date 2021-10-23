```
   _____ _                        __     
  / ___/(_)___ _____  ____ ______/ /_  __
  \__ \/ / __ `/ __ \/ __ `/ ___/ / / / /
 ___/ / / /_/ / / / / /_/ / /  / / /_/ / 
/____/_/\__, /_/ /_/\__,_/_/  /_/\__, /  
       /____/                   /____/   
```
Signarly is a cryptocurrency trading bot.

P.S Signarly is currently on a dry run (mirroring the market). Watch for the upcoming updates on the next steps section.  
## Requirements
- Python 3.7 or higher.
#### - Install pipenv
```Python
    pip install pipenv
```
#### - Access project director
```Python
    cd signarly/
```
#### - Install requirements
```Python
    pipenv shell
```
```Python
    pipenv install
```
## Usage
```
Version - Alpha 1.0.0
usage: bot.py [-h] [--coin COIN] [--stable-coin STABLE_COIN] [--budget BUDGET] [--gain_percentage GAIN_PERCENTAGE] [--loss_percentage LOSS_PERCENTAGE]

Signarly TradingBot Command Line.

optional arguments:
  -h, --help            show this help message and exit
  --coin COIN           Select the cryptocurrency you want to trade.
  --stable-coin STABLE_COIN
                        Select the stable coin you want to trade against.
  --budget BUDGET       Select the budget you want to start with.
  --gain_percentage GAIN_PERCENTAGE
                        Select the price percentage increase above which you want the bot to cash out.
  --loss_percentage LOSS_PERCENTAGE
                        Select the price percentage decrease below which you want the bot to cut losses.
```
## Example
```Python
    python bot.py --coin BNB --stable-coin USDT --budget 2000 --gain_percentage 0.2 --loss_percentage 0.05
```
## Next steps
- Add Wallet embeddings
- Add more technical indicators
- Add more trading strategies
- Implement unit tests
- Implement CI/CD
