import sys
from botchart import BotChart
from botstrategy import BotStrategy
import time

def main(argv):
	#chart = BotChart("poloniex","BTC_ETH")

	strategy = BotStrategy()

	t_end = time.time() + (60*60*7)

	while time.time() < t_end:
		strategy.tick()

if __name__ == "__main__":
	main(sys.argv[1:])
