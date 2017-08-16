# Cryptocurrency Trading System
Cryptocurrency Trading System focused on the BTC to ETH currency pair utilizing the poloniex API wrapper

Buy indicators: 

   1. Buy when current eth sentiment is greather than 7.5% than historical eth sentiment
   
   2. Buy when current btc sentiment is lower than 7.5% than historical btc sentiment
   
   3. Buy when current btc sentiment is lower than 5% and eth sentiment is greater than 5%

Sell indicators:
   1. Sell eth when the (recent sentiment - historical)/100 is less than ?
   
   2. Sell btc when the (recent sentiment - historical)/100 is greater than or equal to 0
   
   3. *add another sell statment if both eth & btc trade type*

*currently figuring out sell percent*
added print statments for btc_change statement

Areas that need work: 

    Sentiment is calculated through nltk, where a given set of positive and negative tweets are given

         Problems with this: 
         1. Testing data set is very incomplete and therefore sentiment is not accurate

         Solutions:
         1. Lexcion based approach may be better but run time will be really high 
         2. Using NLP to figure out sentiment without given test tweets


Areas that can be implemented:

2. Incorporate multiple currency pairs
3. Sentiment of various cryptos, highest ones are traded

