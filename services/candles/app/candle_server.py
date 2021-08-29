from os import environ
from signal import signal, SIGINT, SIGTERM
from time import time
from zmq import Context, ROUTER
from orjson import loads, dumps
from traceback import format_exc

from google.cloud.error_reporting import Client as ErrorReportingClient

from components.ccxt import CCXT
from components.iexc import IEXC


class CandleProcessor(object):
	stableCoinTickers = ["USD", "USDT", "USDC", "DAI", "HUSD", "TUSD", "PAX", "USDK", "USDN", "BUSD", "GUSD", "USDS"]

	def __init__(self):
		self.isServiceAvailable = True
		signal(SIGINT, self.exit_gracefully)
		signal(SIGTERM, self.exit_gracefully)

		self.logging = ErrorReportingClient(service="candle_server")

		self.context = Context.instance()
		self.socket = self.context.socket(ROUTER)
		self.socket.bind("tcp://*:6900")

		print("[Startup]: Candle Server is online")

	def exit_gracefully(self):
		print("[Startup]: Candle Server is exiting")
		self.socket.close()
		self.isServiceAvailable = False

	def run(self):
		while self.isServiceAvailable:
			try:
				response = [dumps({}), b""]
				message = self.socket.recv_multipart()
				if len(message) != 5: continue
				origin, delimeter, clientId, service, request = message
				request = loads(request)
				if request.get("timestamp") + 60 < time():
					print("Request received too late")
					continue

				if service == b"candle":
					response = self.request_candle(request)

			except (KeyboardInterrupt, SystemExit): return
			except Exception:
				print(format_exc())
				print(request)
				if environ["PRODUCTION_MODE"]: self.logging.report_exception()
			finally:
				try: self.socket.send_multipart([origin, delimeter] + response)
				except: pass
				request = None

	def request_candle(self, request):
		payload, candleMessage, updatedCandleMessage = {}, "", ""

		for platform in request["platforms"]:
			currentRequest = request.get(platform)

			if platform == "CCXT":
				payload, updatedCandleMessage = CCXT.request_candles(currentRequest)
			elif platform == "IEXC":
				payload, updatedCandleMessage = IEXC.request_candles(currentRequest)
			elif platform == "Serum":
				pass

			if bool(payload):
				return [dumps(payload), updatedCandleMessage.encode()]
			elif updatedCandleMessage != "":
				candleMessage = updatedCandleMessage

		return [dumps({}), candleMessage.encode()]

if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	print("[Startup]: Candle Server is in startup, running in {} mode.".format("production" if environ["PRODUCTION_MODE"] else "development"))
	candleServer = CandleProcessor()
	candleServer.run()