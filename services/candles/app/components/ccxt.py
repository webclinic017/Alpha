from TickerParser import Exchange
from components.abstract import AbstractProvider


class CCXT(AbstractProvider):
	@classmethod
	def request_candles(cls, request):
		ticker = request.get("ticker")
		exchange = Exchange.from_dict(ticker.get("exchange"))

		if exchange is None: return [{}, ""]

		try:
			rawData = exchange.properties.fetch_ohlcv(ticker.get("symbol"), timeframe="1m", limit=3)
			if len(rawData) == 0 or rawData[-1][4] is None or rawData[0][1] is None: return [{}, ""]
		except:
			return [{}, ""]

		payload = {
			"candles": [],
			"title": ticker.get("name"),
			"sourceText": "Data from {}".format(exchange.name),
			"platform": "CCXT"
		}

		for e in rawData:
			timestamp = e[0] / 1000
			if ticker.get("isReversed"):
				payload["candles"].append([timestamp, 1 / e[1], 1 / e[2], 1 / e[3], 1 / e[4]])
			else:
				payload["candles"].append([timestamp, e[1], e[2], e[3], e[4]])

		return [payload, ""]