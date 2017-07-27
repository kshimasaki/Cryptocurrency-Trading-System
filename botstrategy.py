from botlog import BotLog
from bottrade import BotTrade
import get_tweets_test
from poloniex import poloniex
import time
import tweepy

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = 0
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.btc_historical_percent = 0
		self.btc_historical_positive = 0
		self.btc_historical_negative = 0
		self.btc_historical_score = 0
		self.btc_historical_total = 0
		self.btc_sinceID = 0
		self.eth_historical_percent = 0
		self.eth_historical_positive = 0
		self.eth_historical_negative = 0
		self.eth_historical_score = 0
		self.eth_historical_total = 0
		self.eth_sinceID = 0
		self.eth_trading_percent = 0

	def tick(self,candlestick):
		self.conn = poloniex('4ZY2C395-6I1FSGK4-HMOBG4CY-40UPC0O7','d8fc1ac2e03619489853fff56356f0a364f2d9a23ecad54f9536763e042226d8d6b3faa6c40b97de0ad5f5413c3d97e05b18d58d74007b96059757593591a1c3')
		self.currentPrice = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
		self.prices = self.currentPrice["BTC_ETH"]['last']

		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)

		self.output.log("Price: "+ str(self.prices)) #+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []


		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):

			bitcoin_query = 'BTC AND Bitcoin'
			btc_tweets, sinceid_recent = get_tweets_test.get_tweets(1,0,bitcoin_query)

			btc_total_score2, btc_positive2, btc_negative2, btc_total2 = get_tweets_test.classify(btc_tweets)

			btc_percent = (btc_positive2/btc_total2)*100

			btc_historical_tweets, self.btc_sinceid = get_tweets_test.get_tweets(10, self.btc_sinceID, bitcoin_query)
			btc_total_score, btc_positive, btc_negative, btc_total = get_tweets_test.classify(btc_historical_tweets)
			self.btc_historical_positive = self.btc_historical_positive + btc_positive
			self.btc_historical_negative = self.btc_historical_negative + btc_negative
			self.btc_historical_score = self.btc_historical_score + btc_total_score
			self.btc_historical_total = self.btc_historical_total + btc_total

			self.btc_historical_percent = (self.btc_historical_positive / self.btc_historical_total) * 100

			ethereum_query = 'Ethereum AND ETH'
			eth_tweets, sinceid_recent = get_tweets_test.get_tweets(1,0,ethereum_query)

			eth_total_score2, eth_positive2, eth_negative2, eth_total2 = get_tweets_test.classify(eth_tweets)
			eth_percent = (eth_positive2/eth_total2)*100

			eth_historical_tweets, self.eth_sinceID = get_tweets_test.get_tweets(10, self.eth_sinceID, ethereum_query)
			eth_total_score, eth_positive, eth_negative, eth_total = get_tweets_test.classify(eth_historical_tweets)
			self.eth_historical_positive = self.eth_historical_percent + eth_positive
			self.eth_historical_negative = self.eth_historical_negative + eth_negative
			self.eth_historical_score = self.eth_historical_score + eth_total_score
			self.eth_historical_total = self.eth_historical_total + eth_total

			self.eth_historical_percent = (self.eth_historical_positive/self.eth_historical_total)*100


			if ((eth_percent > 1.04*self.eth_historical_percent and  eth_percent > 50) and btc_percent < 0.95*self.btc_historical_percent):

				self.eth_trading_percent = eth_percent


				self.trades.append(BotTrade(self.prices,stopLoss= 0.001))

				time.sleep(60*3)

			else:
				time.sleep(60*7)

		for trade in openTrades:


			bitcoin_query = 'BTC AND Bitcoin'
			btc_tweets, sinceid_recent = get_tweets_test.get_tweets(1,0,bitcoin_query)

			btc_total_score2, btc_positive2, btc_negative2, btc_total2 = get_tweets_test.classify(btc_tweets)
			#
			btc_percent = (btc_positive2/btc_total2)*100

			btc_historical_tweets, self.btc_sinceid = get_tweets_test.get_tweets(10, self.btc_sinceID, bitcoin_query)
			btc_total_score, btc_positive, btc_negative, btc_total = get_tweets_test.classify(btc_historical_tweets)
			self.btc_historical_positive = self.btc_historical_positive + btc_positive
			self.btc_historical_negative = self.btc_historical_negative + btc_negative
			self.btc_historical_score = self.btc_historical_score + btc_total_score
			self.btc_historical_total = self.btc_historical_total + btc_total

			self.btc_historical_percent = (self.btc_historical_positive / self.btc_historical_total) * 100

			ethereum_query = 'Ethereum AND ETH'
			eth_tweets, sinceid_recent = get_tweets_test.get_tweets(1,0,ethereum_query)

			eth_total_score2, eth_positive2, eth_negative2, eth_total2 = get_tweets_test.classify(eth_tweets)
			eth_percent = (eth_positive2/eth_total2)*100

			eth_historical_tweets, self.eth_sinceID = get_tweets_test.get_tweets(10, self.eth_sinceID, ethereum_query)
			eth_total_score, eth_positive, eth_negative, eth_total = get_tweets_test.classify(eth_historical_tweets)
			self.eth_historical_positive = self.eth_historical_percent + eth_positive
			self.eth_historical_negative = self.eth_historical_negative + eth_negative
			self.eth_historical_score = self.eth_historical_score + eth_total_score
			self.eth_historical_total = self.eth_historical_total + eth_total

			self.eth_historical_percent = (self.eth_historical_positive/self.eth_historical_total)*100

			if (eth_percent < 0.95*self.eth_trading_percent or btc_percent > 1.04*self.btc_historical_percent):
				price = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
				self.currentClose = price["BTC_ETH"]['last']
				trade.close(self.currentClose)
			else:
				time.sleep(60*7)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
