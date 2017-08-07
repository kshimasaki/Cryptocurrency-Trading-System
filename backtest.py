import sys
from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	#chart = BotChart("poloniex","BTC_ETH")

	strategy = BotStrategy()

	for i in range(1000):
		strategy.tick()

if __name__ == "__main__":
	main(sys.argv[1:])
