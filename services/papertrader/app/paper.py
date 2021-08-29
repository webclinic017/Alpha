from os import environ
from signal import signal, SIGINT, SIGTERM
from time import time, sleep
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from pytz import utc
from traceback import format_exc
from zmq import Context, Poller, REQ, LINGER, POLLIN
from orjson import dumps, loads, OPT_SORT_KEYS

from google.cloud.firestore import Client as FirestoreClient
from google.cloud.error_reporting import Client as ErrorReportingClient

from DatabaseConnector import DatabaseConnectorSync as DatabaseConnector
from helpers.utils import Utils


database = FirestoreClient()


class PaperTraderServer(object):
	accountProperties = DatabaseConnector(mode="account")
	registeredAccounts = {}

	zmqContext = Context.instance()


	# -------------------------
	# Startup
	# -------------------------
	
	def __init__(self):
		self.isServiceAvailable = True
		signal(SIGINT, self.exit_gracefully)
		signal(SIGTERM, self.exit_gracefully)

		self.logging = ErrorReportingClient(service="paper_trader")

		self.cache = {}

	def exit_gracefully(self):
		print("[Startup]: Paper Trader Server handler is exiting")
		self.isServiceAvailable = False


	# -------------------------
	# Job queue
	# -------------------------

	def run(self):
		while self.isServiceAvailable:
			try:
				sleep(Utils.seconds_until_cycle())
				t = datetime.now().astimezone(utc)
				timeframes = Utils.get_accepted_timeframes(t)

				if "1m" in timeframes:
					self.update_accounts()
					self.process_paper_limit_orders()

			except (KeyboardInterrupt, SystemExit): return
			except Exception:
				print(format_exc())
				if environ["PRODUCTION_MODE"]: self.logging.report_exception()

	def update_accounts(self):
		try:
			self.registeredAccounts = self.accountProperties.keys()
		except (KeyboardInterrupt, SystemExit): pass
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception()


	# -------------------------
	# Paper trading
	# -------------------------

	def process_paper_limit_orders(self):
		try:
			self.cache = {}
			users = database.document("details/openPaperOrders").collections()
			with ThreadPoolExecutor(max_workers=20) as pool:
				for user in users:
					accountId = user.id
					authorId = self.registeredAccounts.get(accountId, accountId)
					if authorId is None: continue
					for order in user.stream():
						pool.submit(self.check_paper_order, authorId, accountId, order.reference, order.id, order.to_dict())

		except (KeyboardInterrupt, SystemExit): pass
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception()

	def check_paper_order(self, authorId, accountId, reference, orderId, order):
		socket = PaperTraderServer.zmqContext.socket(REQ)
		socket.connect("tcp://candle-server:6900")
		socket.setsockopt(LINGER, 3)
		poller = Poller()
		poller.register(socket, POLLIN)

		try:
			currentPlatform = order["request"].get("currentPlatform")
			currentRequest = order["request"].get(currentPlatform)
			ticker = currentRequest.get("ticker")
			hashName = hash(dumps(ticker, option=OPT_SORT_KEYS))

			if order["timestamp"] < time() - 86400 * 30.5 * 3:
				if environ["PRODUCTION_MODE"]:
					database.document("discord/properties/messages/{}".format(str(uuid4()))).set({
						"title": "Paper {} order of {} {} at {} {} expired.".format(order["orderType"].replace("-", " "), order["amountText"], ticker.get("base"), order["price"], ticker.get("quote")),
						"subtitle": "Alpha Paper Trader",
						"description": "Paper orders automatically cancel after 3 months. If you'd like to keep your order, you'll have to set it again.",
						"color": 6765239,
						"user": authorId,
						"channel": order["channel"]
					})
					reference.delete()

				else:
					print("{}: paper {} order of {} {} at {} expired".format(order["orderType"].replace("-", " "), order["amountText"], ticker.get("base"), order["price"], ticker.get("quote")))

			else:
				if hashName in self.cache:
					payload = self.cache.get(hashName)
				else:
					order["request"]["timestamp"] = time()
					order["request"]["authorId"] = authorId
					socket.send_multipart([b"papertrader", b"candle", dumps(order["request"])])
					responses = poller.poll(30 * 1000)

					if len(responses) != 0:
						[payload, responseText] = socket.recv_multipart()
						payload = loads(payload)
						responseText = responseText.decode()

						if not bool(payload):
							if responseText != "":
								print("Paper order request error:", responseText)
								if environ["PRODUCTION_MODE"]: self.logging.report(responseText)
							return

						self.cache[hashName] = payload
					else:
						raise Exception("time out")

				accountProperties = self.accountProperties.get(accountId)

				for candle in reversed(payload["candles"]):
					if candle[0] < order["timestamp"] / 1000: break
					if (order["placement"] == "below" and candle[3] is not None and candle[3] <= order["price"]) or (order["placement"] == "above" and candle[2] is not None and order["price"] <= candle[2]):
						if environ["PRODUCTION_MODE"]:
							base = ticker.get("base")
							quote = ticker.get("quote")
							if base in ["USD", "USDT", "USDC", "DAI", "HUSD", "TUSD", "PAX", "USDK", "USDN", "BUSD", "GUSD", "USDS"]:
								baseBalance = accountProperties["paperTrader"]["balance"]
								base = "USD"
							else:
								baseBalance = accountProperties["paperTrader"]["balance"][currentPlatform]
							if quote in ["USD", "USDT", "USDC", "DAI", "HUSD", "TUSD", "PAX", "USDK", "USDN", "BUSD", "GUSD", "USDS"]:
								quoteBalance = accountProperties["paperTrader"]["balance"]
								quote = "USD"
							else:
								quoteBalance = accountProperties["paperTrader"]["balance"][currentPlatform]

							execAmount = order["amount"]
							if order["orderType"] == "buy":
								baseBalance[base] = baseBalance.get(base, 0) + execAmount

							elif order["orderType"] == "sell":
								quoteBalance[quote] = quoteBalance.get(quote, 0) + execAmount * order["price"]

							elif order["orderType"] == "stop-buy":
								execAmount = min(abs(quoteBalance.get(quote, 0)), order["price"] * execAmount) / order["price"]
								baseBalance[base] = baseBalance.get(base, 0) + execAmount
								quoteBalance[quote] = quoteBalance.get(quote, 0) - order["price"] * execAmount

							elif order["orderType"] == "stop-sell":
								execAmount = min(abs(baseBalance.get(base, 0)), execAmount)
								baseBalance[base] = baseBalance.get(base, 0) - execAmount
								quoteBalance[quote] = quoteBalance.get(quote, 0) + execAmount * order["price"]

							order["status"] = "filled"
							database.document("details/paperOrderHistory/{}/{}".format(accountId, orderId)).set(order)
							database.document("accounts/{}".format(accountId)).set({"paperTrader": accountProperties["paperTrader"]}, merge=True)

							database.document("discord/properties/messages/{}".format(str(uuid4()))).set({
								"title": "Paper {} order of {} {} at {} {} was successfully executed.".format(order["orderType"].replace("-", " "), order["amountText"], ticker.get("base"), order["price"], ticker.get("quote")),
								"subtitle": "Alpha Paper Trader",
								"color": 6765239,
								"user": authorId
							})
							reference.delete()

						else:
							print("{}: paper {} order of {} {} at {} {} was successfully executed".format(accountId, order["orderType"].replace("-", " "), order["amountText"], ticker.get("base"), order["price"], ticker.get("quote")))
						break

		except (KeyboardInterrupt, SystemExit): pass
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=f"{accountId}, {authorId}")


if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	print("[Startup]: Paper Trader Server is in startup, running in {} mode.".format("production" if environ["PRODUCTION_MODE"] else "development"))

	if not environ["PRODUCTION_MODE"]: exit(0)
	paperTraderServer = PaperTraderServer()
	paperTraderServer.run()
