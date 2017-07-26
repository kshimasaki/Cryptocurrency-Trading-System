from poloniex import poloniex

class BotChart(object):
	def __init__(self, exchange, pair): #,period):
		self.conn = poloniex('4ZY2C395-6I1FSGK4-HMOBG4CY-40UPC0O7','d8fc1ac2e03619489853fff56356f0a364f2d9a23ecad54f9536763e042226d8d6b3faa6c40b97de0ad5f5413c3d97e05b18d58d74007b96059757593591a1c3')

		self.pair = pair
		#self.period = period

		#self.startTime = 1491048000
		#self.endTime = 1491591200

		self.data = self.conn.api_query("returnTicker",{"currencyPair":self.pair}) #"start":self.startTime,"end":self.endTime,"period":self.period})

	def getPoints(self):

		#print self.data.last
		return self.data.last
