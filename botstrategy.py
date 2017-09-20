from botlog import BotLog
from bottrade import BotTrade
import tweets
import time
from bittrex import bittrex
import numpy as np
import math

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
		self.api = bittrex('','')
		self.btc_sentiments = []
		self.eth_sentiments = []

	def tick(self):

		currentPrice = self.api.getticker('BTC-ETH')
		self.prices = currentPrice['Ask']

		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)

		self.output.log("Price: "+ '{0:.8f}'.format(self.prices))

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

				btc_historical_tweets, self.btc_sinceid = tweets.get_tweets(50, self.btc_sinceID, bitcoin_query)
				btc_total_score, btc_positive, btc_negative, btc_total = tweets.classify(btc_historical_tweets)
				self.btc_historical_positive = self.btc_historical_positive + btc_positive
				self.btc_historical_negative = self.btc_historical_negative + btc_negative
				self.btc_historical_score = self.btc_historical_score + btc_total_score
				self.btc_historical_total = self.btc_historical_total + btc_total

				self.btc_historical_percent = (self.btc_historical_positive / self.btc_historical_total) * 100

				ethereum_query = 'Ethereum OR ETH OR $ETH'

				eth_historical_tweets, self.eth_sinceID = tweets.get_tweets(50, self.eth_sinceID, ethereum_query)
				eth_total_score, eth_positive, eth_negative, eth_total = tweets.classify(eth_historical_tweets)
				self.eth_historical_positive = self.eth_historical_positive + eth_positive
				self.eth_historical_negative = self.eth_historical_negative + eth_negative
				self.eth_historical_score = self.eth_historical_score + eth_total_score
				self.eth_historical_total = self.eth_historical_total + eth_total

				self.eth_historical_percent = (self.eth_historical_positive/self.eth_historical_total)*100

				if self.btc_historical_total >= 100000:
					print '\033[1m' + "Historical Tweets Analyzed"
					print "historical btc percent: " + str(self.btc_historical_percent)
					print "historical eth percent: " + str(self.eth_historical_percent)
					print '\033[0m'

			elif (self.btc_historical_total > 100000):
				bitcoin_query = 'BTC OR Bitcoin OR $BTC'

				btc_tweets, sinceid_recent = tweets.get_tweets(50,0,bitcoin_query)
				btc_total_score2, btc_positive2, btc_negative2, btc_total2 = tweets.classify(btc_tweets)
				btc_percent = (btc_positive2/btc_total2)*100

				ethereum_query = 'Ethereum OR ETH OR $ETH'

				eth_tweets, sinceid_recent = tweets.get_tweets(50,0,ethereum_query)
				eth_total_score2, eth_positive2, eth_negative2, eth_total2 = tweets.classify(eth_tweets)
				eth_percent = (eth_positive2/eth_total2)*100

				if(eth_percent > 1.042 *self.eth_historical_percent or btc_percent < 0.943*self.btc_historical_percent):

					if btc_percent < 0.943*self.btc_historical_percent:
						self.btc_sentiments = []
						self.btc_trading_percent = btc_percent
						self.type_of_trade = 'BTC'
						self.trades.append(BotTrade(self.prices,stopLoss= 0.01))
					elif(eth_percent > 1.042*self.eth_historical_percent):
						self.eth_sentiments = []
						self.eth_trading_percent = eth_percent
						self.type_of_trade = 'ETH'
						self.trades.append(BotTrade(self.prices,stopLoss= 0.01))
					else:
						self.type_of_trade = ''

				time.sleep(60*5)

		for trade in openTrades:

			if (self.type_of_trade == 'BTC'):

				bitcoin_query = 'BTC OR Bitcoin OR $BTC'
				btc_tweets, sinceid_recent = tweets.get_tweets(10,0,bitcoin_query)

				btc_total_score2, btc_positive2, btc_negative2, btc_total2 = tweets.classify(btc_tweets)
				btc_percent = (btc_positive2/btc_total2)*100

				self.btc_sentiments.append(btc_percent)

				if (len(self.btc_sentiments) > 5):

					mean_sentiment = np.mean(self.btc_sentiments)
					std_sentiment = np.std(self.btc_sentiments)

					if btc_percent >= mean_sentiment + ((0.800 * std_sentiment)/math.sqrt(len(self.btc_sentiments))) :
						price = self.api.getticker('BTC-ETH')
						self.currentClose = price['Bid']
						trade.close(self.currentClose)
				else:
					time.sleep(60*3)

			elif (self.type_of_trade == 'ETH'):

				ethereum_query = 'Ethereum OR ETH OR $ETH'
				eth_tweets, sinceid_recent = tweets.get_tweets(10,0,ethereum_query)

				eth_total_score2, eth_positive2, eth_negative2, eth_total2 = tweets.classify(eth_tweets)
				eth_percent = (eth_positive2/eth_total2)*100

				self.eth_sentiments.append(eth_percent)

				if (len(self.eth_sentiments) > 5):

					mean_sentiment = np.mean(self.eth_sentiments)
					std_sentiment = np.std(self.eth_sentiments)

					if eth_percent <= mean_sentiment - ((0.674 * std_sentiment)/math.sqrt(len(self.eth_sentiments))) :
						price = self.api.getticker('BTC-ETH')
						self.currentClose = price['Bid']
						trade.close(self.currentClose)
				else:
					time.sleep(60*3)
			else:
				price = self.api.getticker('BTC-ETH')
				self.currentClose = price['Bid']
				trade.close(self.currentClose)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.prices)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
