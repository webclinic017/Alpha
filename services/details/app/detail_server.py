from os import environ
from signal import signal, SIGINT, SIGTERM
from time import time
from uuid import uuid4
from zmq import Context, ROUTER
from orjson import dumps, loads
from traceback import format_exc

from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import ArrayUnion
from google.cloud.error_reporting import Client as ErrorReportingClient

from components.coingecko import CoinGecko
from components.iexc import IEXC


database = FirestoreClient()


class DetailProcessor(object):
	def __init__(self):
		self.isServiceAvailable = True
		signal(SIGINT, self.exit_gracefully)
		signal(SIGTERM, self.exit_gracefully)

		self.logging = ErrorReportingClient(service="details_server")

		self.context = Context.instance()
		self.socket = self.context.socket(ROUTER)
		self.socket.bind("tcp://*:6900")

		print("[Startup]: Detail Server is online")

	def exit_gracefully(self):
		print("[Startup]: Detail Server is exiting")
		self.socket.close()
		self.isServiceAvailable = False

	def run(self):
		while self.isServiceAvailable:
			try:
				response = [dumps({}),  b""]
				message = self.socket.recv_multipart()
				if len(message) != 5: continue
				origin, delimeter, clientId, service, request = message
				request = loads(request)
				if request.get("timestamp") + 60 < time():
					print("Request received too late")
					continue

				if service == b"detail":
					response = self.request_detail(request, clientId)

			except (KeyboardInterrupt, SystemExit): return
			except Exception:
				print(format_exc())
				print(request)
				if environ["PRODUCTION_MODE"]: self.logging.report_exception()
			finally:
				try: self.socket.send_multipart([origin, delimeter] + response)
				except: pass
				request = None

	def request_detail(self, request, clientId):
		payload, tradeMessage, updatedTradeMessage = {}, "", ""

		for platform in request["platforms"]:
			currentRequest = request.get(platform)

			if platform == "CoinGecko":
				payload, updatedQuoteMessage = CoinGecko.request_details(currentRequest)
			elif platform == "IEXC":
				payload, updatedQuoteMessage = IEXC.request_details(currentRequest)

			if bool(payload):
				if clientId in [b"discord_alpha"] and currentRequest["ticker"].get("base") is not None:
					database.document("dataserver/statistics/{}/{}".format(currentRequest.get("parserBias"), int(time() // 3600 * 3600))).set({
						currentRequest["ticker"].get("base"): ArrayUnion([str(request.get("authorId"))]),
					}, merge=True)
				return [dumps(payload), updatedTradeMessage.encode()]
			elif updatedTradeMessage != "":
				tradeMessage = updatedTradeMessage

		return [dumps({}), tradeMessage.encode()]

if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	print("[Startup]: Detail Server is in startup, running in {} mode.".format("production" if environ["PRODUCTION_MODE"] else "development"))
	detailServer = DetailProcessor()
	detailServer.run()