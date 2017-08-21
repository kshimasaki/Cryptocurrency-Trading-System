# Cryptocurrency Trading System
Cryptocurrency Trading System focused on the BTC to ETH currency pair utilizing the bittrex API wrapper

*bittrex api wrapper: https://github.com/ndri/python-bittrex *

Steps:
1. Query 100,000 tweets to calculate historical sentiment of BTC & ETH
2. Query 500 recent tweets to calculate current sentiment of BTC & ETH
3. See if any of the buy conditions are achieved + note down the type of trade
4. Query 500 recent tweets to calculate current sentiment of BTC & ETH
5. See if corresponding sell condition is achieved 

Buy indicators: 

   1. Buy when current eth sentiment is greather than 5% than historical eth sentiment
   
   2. Buy when current btc sentiment is lower than 5% than historical btc sentiment
   
   3. Buy when current btc sentiment is lower than 5% and eth sentiment is greater than 5%

Sell indicators:
   1. Sell eth trade when the percent change of sentiment is less than 2.2%
   
   2. Sell btc trade when the percent change of sentiment is greater than 2.2%
   
   3. Sell ethbtc trade when eth sentiment change is less than 2.2% and btc sentiment change is greater than 2.2%

*currently figuring out sell percent*

Areas that need work: 

1. Buying and selling conditions
2. NLP  

Areas that can be implemented:

2. Incorporate multiple currency pairs
3. Sentiment of various cryptos, highest ones are traded
