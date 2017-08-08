# Cryptocurrency Trading System
Cryptocurrency Trading System focused on the BTC to ETH currency pair utilizing the poloniex API wrapper

Buy indicators: 

   1. Buy when current eth sentiment is greather than 7.5% than historical eth sentiment
   
   2. Buy when current btc sentiment is lower than 7.5% than historical btc sentiment

Sell indicators:
   1. Sell when current eth sentiment is 5% lower than eth trading percent
   
   2. Sell when current btc sentiment is 5% lower than btc trading percent


Sentiment is calculated through nltk, where a given set of positive and negative tweets are given

Problems with this: 
1. Testing data set is very incomplete and therefore sentiment is not accurate

Solutions:
1. Lexcion based approach may be better but run time will be really high 
