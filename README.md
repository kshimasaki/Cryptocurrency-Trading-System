# Cryptocurrency Trading System
Cryptocurrency Trading System focused on the BTC to ETH currency pair utilizing the poloniex API wrapper

Buy indicators: 

   1. Buy when current eth sentiment is greather than 2.2% than historical eth sentiment
   
   2. Buy when current btc sentiment is lower than 3% than historical btc sentiment
   
   3. Buy when current btc sentiment is lower than 3% and eth sentiment is greater than 2.2%

Sell indicators:
   1. Sell eth when the (recent sentiment - historical)/100 is less than ?
   
   2. Sell btc when the (recent sentiment - historical)/100 is greater than ?
   
   3. *add another sell statment if both eth & btc trade type*

*currently figuring out sell percent*

Areas that need work: 

1. Buying and selling conditions
2. NLP  

Areas that can be implemented:

2. Incorporate multiple currency pairs
3. Sentiment of various cryptos, highest ones are traded

