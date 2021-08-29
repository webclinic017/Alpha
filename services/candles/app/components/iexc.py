from os import environ
from datetime import datetime
from pytz import timezone
from requests import get

from iexfinance.stocks import Stock

from TickerParser import Exchange
from components.abstract import AbstractProvider


class IEXC(AbstractProvider):
	@classmethod
	def request_candles(cls, request):
		ticker = request.get("ticker")
		exchange = Exchange.from_dict(ticker.get("exchange"))

		try:
			stock = Stock(ticker.get("id"), token=environ["IEXC_KEY"])
			rawData = stock.get_intraday_prices(chartLast=3)
			if len(rawData) == 0: return [{}, ""]
			if ticker.get("quote") is None and exchange is not None: return [{}, "Price for `{}` is not available on {}.".format(ticker.get("name"), exchange.get("name"))]
		except:
			return [{}, ""]

		payload = {
			"candles": [],
			"title": ticker.get("name"),
			"sourceText": "Data provided by IEX Cloud",
			"platform": "IEXC"
		}

		for index, e in rawData.iterrows():
			parsedDatetime = None
			try: parsedDatetime = datetime.strptime(index, "%Y-%m-%d %I:%M %p")
			except: pass
			try: parsedDatetime = datetime.strptime(index, "%Y-%m-%d %I %p")
			except: pass
			try: parsedDatetime = datetime.strptime(index, "%Y-%m-%d None")
			except: pass

			if parsedDatetime is None:
				raise Exception("timestamp formatting mismatch: {}".format(index))

			timestamp = timezone('US/Eastern').localize(parsedDatetime, is_dst=None).timestamp()

			if ticker.get("isReversed"):
				if "marketClose" in e:
					payload["candles"].append([timestamp, 1 / e.marketOpen, 1 / e.marketHigh, 1 / e.marketLow, 1 / e.marketClose])
				else:
					payload["candles"].append([timestamp, 1 / e.open, 1 / e.high, 1 / e.low, 1 / e.close])
			else:
				if "marketClose" in e:
					payload["candles"].append([timestamp, e.marketOpen, e.marketHigh, e.marketLow, e.marketClose])
				else:
					payload["candles"].append([timestamp, e.open, e.high, e.low, e.close])

		return [payload, ""]