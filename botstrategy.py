from botlog import BotLog
from bottrade import BotTrade
import tweets
from poloniex import poloniex
import time


class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = 0
		self.trades = []
		self.currentClose = ""
		self.numSimulTrades = 1
		self.btc_historical_percent = 0
		self.btc_historical_positive = 0
		self.btc_historical_negative = 0
		self.btc_historical_score = 0
		self.btc_historical_total = 0
		self.btc_sinceID = 0
		self.btc_trading_percent = 0
		self.eth_historical_percent = 0
		self.eth_historical_positive = 0
		self.eth_historical_negative = 0
		self.eth_historical_score = 0
		self.eth_historical_total = 0
		self.eth_sinceID = 0
		self.eth_trading_percent = 0
		self.type_of_trade = ''

	def tick(self):
		self.conn = poloniex('4ZY2C395-6I1FSGK4-HMOBG4CY-40UPC0O7','d8fc1ac2e03619489853fff56356f0a364f2d9a23ecad54f9536763e042226d8d6b3faa6c40b97de0ad5f5413c3d97e05b18d58d74007b96059757593591a1c3')
		currentPrice = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
		self.prices = currentPrice["BTC_ETH"]['last']

		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)

		self.output.log("Price: "+ str(self.prices))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.btc_historical_total <= 100000):
				bitcoin_query = 'BTC OR Bitcoin OR $BTC'

				btc_historical_tweets, self.btc_sinceid = tweets.get_tweets(10, self.btc_sinceID, bitcoin_query)
				btc_total_score, btc_positive, btc_negative, btc_total = tweets.classify(btc_historical_tweets)
				self.btc_historical_positive = self.btc_historical_positive + btc_positive
				self.btc_historical_negative = self.btc_historical_negative + btc_negative
				self.btc_historical_score = self.btc_historical_score + btc_total_score
				self.btc_historical_total = self.btc_historical_total + btc_total

				self.btc_historical_percent = (self.btc_historical_positive / self.btc_historical_total) * 100

				ethereum_query = 'Ethereum OR ETH OR $ETH'

				eth_historical_tweets, self.eth_sinceID = tweets.get_tweets(10, self.eth_sinceID, ethereum_query)
				eth_total_score, eth_positive, eth_negative, eth_total = tweets.classify(eth_historical_tweets)
				self.eth_historical_positive = self.eth_historical_positive + eth_positive
				self.eth_historical_negative = self.eth_historical_negative + eth_negative
				self.eth_historical_score = self.eth_historical_score + eth_total_score
				self.eth_historical_total = self.eth_historical_total + eth_total

				self.eth_historical_percent = (self.eth_historical_positive/self.eth_historical_total)*100
				
			elif (self.btc_historical_total > 100000):
				bitcoin_query = 'BTC OR Bitcoin OR $BTC'

				btc_tweets, sinceid_recent = tweets.get_tweets(5,0,bitcoin_query)
				btc_total_score2, btc_positive2, btc_negative2, btc_total2 = tweets.classify(btc_tweets)
				btc_percent = (btc_positive2/btc_total2)*100

				ethereum_query = 'Ethereum OR ETH OR $ETH'

				eth_tweets, sinceid_recent = tweets.get_tweets(5,0,ethereum_query)
				eth_total_score2, eth_positive2, eth_negative2, eth_total2 = tweets.classify(eth_tweets)
				eth_percent = (eth_positive2/eth_total2)*100

				if((eth_percent > 1.05*self.eth_historical_percent and  eth_percent > 50) or btc_percent < 0.95*self.btc_historical_percent):

					if btc_percent < 0.95*self.btc_historical_percent:
						self.btc_trading_percent = btc_percent
						self.type_of_trade = 'BTC'
						self.trades.append(BotTrade(self.prices,stopLoss= 0.01))
					elif(eth_percent > 1.05*self.eth_historical_percent and  eth_percent > 50):
						self.eth_trading_percent = eth_percent
						self.type_of_trade = 'ETH'
						self.trades.append(BotTrade(self.prices,stopLoss= 0.01))
					elif (eth_percent > 1.05*self.eth_historical_percent and  eth_percent > 50) and btc_percent < 0.95*self.btc_historical_percent:
						self.eth_trading_percent = eth_percent
						self.type_of_trade = 'BTCETH'
						self.trades.append(BotTrade(self.prices,stopLoss= 0.01))
					else:
						self.type_of_trade = ''

		for trade in openTrades:

			if (self.type_of_trade == 'BTC'):

				bitcoin_query = 'BTC OR Bitcoin OR $BTC'
				btc_tweets, sinceid_recent = tweets.get_tweets(5,0,bitcoin_query)

				btc_total_score2, btc_positive2, btc_negative2, btc_total2 = tweets.classify(btc_tweets)
				btc_percent = (btc_positive2/btc_total2)*100

				btc_change = (btc_percent - self.btc_trading_percent)/(self.btc_historical_percent)
				btc_change = btc_change * 100

				print "btc change: " + str(btc_change)
				if (btc_change >= 2.2):
					price = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
					self.currentClose = price["BTC_ETH"]['last']
					trade.close(self.currentClose)
				else:
					time.sleep(60)

			elif (self.type_of_trade == 'ETH'):

				ethereum_query = 'Ethereum OR ETH OR $ETH'
				eth_tweets, sinceid_recent = tweets.get_tweets(5,0,ethereum_query)

				eth_total_score2, eth_positive2, eth_negative2, eth_total2 = tweets.classify(eth_tweets)
				eth_percent = (eth_positive2/eth_total2)*100

				eth_change = (eth_percent - self.eth_trading_percent)/(self.eth_historical_percent)
				eth_change = eth_change * 100

				print "eth change: " + str(eth_change)
				if (eth_change <= -2.2):
					price = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
					self.currentClose = price["BTC_ETH"]['last']
					trade.close(self.currentClose)
				else:
					time.sleep(60)

			elif (self.type_of_trade == 'BTCETH'):
				bitcoin_query = 'BTC OR Bitcoin OR $BTC'
				btc_tweets, sinceid_recent = tweets.get_tweets(5,0,bitcoin_query)

				btc_total_score2, btc_positive2, btc_negative2, btc_total2 = tweets.classify(btc_tweets)
				btc_percent = (btc_positive2/btc_total2)*100

				btc_change = (btc_percent - self.btc_trading_percent)/(self.btc_historical_percent)
				btc_change = btc_change * 100

				ethereum_query = 'Ethereum OR ETH OR $ETH'
				eth_tweets, sinceid_recent = tweets.get_tweets(5,0,ethereum_query)

				eth_total_score2, eth_positive2, eth_negative2, eth_total2 = tweets.classify(eth_tweets)
				eth_percent = (eth_positive2/eth_total2)*100

				eth_change = (eth_percent - self.eth_trading_percent)/(self.eth_historical_percent)
				eth_change = eth_change * 100

				print "btc change: " + str(btc_change) + " , eth change: " + str(eth_change)

				if (eth_change <= -2.2 and btc_change >= 2.2):
					price = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
					self.currentClose = price["BTC_ETH"]['last']
					trade.close(self.currentClose)
				else:
					time.sleep(60)


			else:
				price = self.conn.api_query("returnTicker",{"currencyPair":'USDT_BTC'})
				self.currentClose = price["BTC_ETH"]['last']
				trade.close(self.currentClose)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.prices)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
