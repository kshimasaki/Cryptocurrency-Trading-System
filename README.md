# Cryptocurrency Trading System


Past research has proven the correlation between the sentiment and price of a stock. This trading system aims to utilize the changes of sentiment surrounding bitcoin and ethereum to predict future trends of the BTC-ETH currency pair. Comparing the sentiment of the last 5,000 tweets to the sentiment of the historical 100,000 tweets provides aids in forumlating a hypothesis of price trends in the near future. 

The python wrapper to connect with the bittrex API is given [here](https://github.com/ndri/python-bittrex)

## Buy indicators: 

   1. Buy ETH when current eth sentiment is greater than 4.2% than historical eth sentiment
   
   2. Buy ETH when current btc sentiment is lower than 5.7% than historical btc sentiment
    
   
   
## Sell indicators: 

Sell indicators are only checked after 30 minutes after buying

   1. Sell ETH when BTC sentiment is 0.800 standard deviations above the mean
   
   2. Sell ETH when ETH sentiment is 0.674 standard deviations below the mean
   
   
