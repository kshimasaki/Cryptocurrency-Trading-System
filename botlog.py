from datetime import datetime

class BotLog(object):
	def __init__(self):
		pass

	def log(self, message):
		today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print "Date: " + str(today) + " " + message
