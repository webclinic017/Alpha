from os import environ
from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from TickerParser import TickerParser
from .parameter import DetailParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("autoDeleteOverride", "autodelete", ["del", "delete", "autodelete"], coingecko="autodelete", iexc="autodelete"),
		Parameter("hideRequest", "hide request", ["hide"], coingecko="hide", iexc="hide")
	]
}
DEFAULTS = {
	"CoinGecko": {
		"preferences": []
	},
	"IEXC": {
		"preferences": []
	}
}


class DetailRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional", **kwargs):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = DetailRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_preferences(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error("`{}` is not a valid argument.".format(argument), isFatal=True)
			elif finalOutput.startswith("`Force Detail"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			if not request.ticker.get("isSimple"):
				request.set_error("Details for aggregated tickers aren't available.", isFatal=True)

			if platform == "CoinGecko":
				pass
			elif platform == "IEXC":
				pass


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class DetailRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}

		self.preferences = []

	async def process_ticker(self):
		updatedTicker, error = None, None
		try: updatedTicker, error = await TickerParser.match_ticker(self.tickerId, None, self.platform, self.parserBias)
		except: pass

		if error is not None:
			self.set_error(error, isFatal=True)
		elif not updatedTicker:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter

	async def add_timeframe(self, argument): raise NotImplementedError

	async def add_exchange(self, argument): raise NotImplementedError

	async def add_style(self, argument): raise NotImplementedError

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"parserBias": self.parserBias,
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences]
		}
		return d