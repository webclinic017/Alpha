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


class AlertsServer(object):
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

		self.logging = ErrorReportingClient(service="alerts")

		self.cache = {}

	def exit_gracefully(self):
		print("[Startup]: Alerts Server handler is exiting")
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
					self.process_price_alerts()

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
	# Price Alerts
	# -------------------------

	def process_price_alerts(self):
		try:
			self.cache = {}
			users = database.document("details/marketAlerts").collections()
			with ThreadPoolExecutor(max_workers=20) as pool:
				for user in users:
					accountId = user.id
					authorId = accountId if accountId.isdigit() else self.registeredAccounts.get(accountId)
					if authorId is None: continue
					for alert in user.stream():
						pool.submit(self.check_price_alert, authorId, accountId, alert.reference, alert.to_dict())

		except (KeyboardInterrupt, SystemExit): pass
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception()

	def check_price_alert(self, authorId, accountId, reference, alert):
		socket = AlertsServer.zmqContext.socket(REQ)
		socket.connect("tcp://candle-server:6900")
		socket.setsockopt(LINGER, 3)
		poller = Poller()
		poller.register(socket, POLLIN)

		try:
			currentPlatform = alert["request"].get("currentPlatform")
			currentRequest = alert["request"].get(currentPlatform)
			ticker = currentRequest.get("ticker")
			hashName = hash(dumps(ticker, option=OPT_SORT_KEYS))

			if alert["timestamp"] < time() - 86400 * 30.5 * 3:
				if environ["PRODUCTION_MODE"]:
					database.document("discord/properties/messages/{}".format(str(uuid4()))).set({
						"title": "Price alert for {} ({}) at {} {} expired.".format(ticker.get("base"), currentPlatform if ticker.get("exchange") is None else ticker.get("exchange").get("name"), alert.get("levelText", alert["level"]), ticker.get("quote")),
						"subtitle": "Price Alerts",
						"description": "Price alerts automatically cancel after 3 months. If you'd like to keep your alert, you'll have to schedule it again.",
						"color": 6765239,
						"user": authorId,
						"channel": alert["channel"]
					})
					reference.delete()

				else:
					print("{}: price alert for {} ({}) at {} {} expired".format(accountId, ticker.get("base"), currentPlatform if ticker.get("exchange") is None else ticker.get("exchange").get("name"), alert.get("levelText", alert["level"]), ticker.get("quote")))

			else:
				if hashName in self.cache:
					payload = self.cache.get(hashName)
				else:
					alert["request"]["timestamp"] = time()
					alert["request"]["authorId"] = authorId
					socket.send_multipart([b"alerts", b"candle", dumps(alert["request"])])
					responses = poller.poll(30 * 1000)

					if len(responses) != 0:
						[payload, responseText] = socket.recv_multipart()
						payload = loads(payload)
						responseText = responseText.decode()

						if not bool(payload):
							if responseText != "":
								print("Alert request error:", responseText)
								if environ["PRODUCTION_MODE"]: self.logging.report(responseText)
							return

						self.cache[hashName] = payload
					else:
						raise Exception("time out")

				for candle in reversed(payload["candles"]):
					if candle[0] < alert["timestamp"]: break
					if (alert["placement"] == "below" and candle[3] is not None and candle[3] <= alert["level"]) or (alert["placement"] == "above" and candle[2] is not None and alert["level"] <= candle[2]):
						if environ["PRODUCTION_MODE"]:
							database.document("discord/properties/messages/{}".format(str(uuid4()))).set({
								"title": "Price of {} ({}) hit {} {}.".format(ticker.get("base"), payload.get("platform") if ticker.get("exchange") is None else ticker.get("exchange").get("name"), alert.get("levelText", alert["level"]), ticker.get("quote")),
								"description": alert.get("triggerMessage"),
								"subtitle": "Price Alerts",
								"color": 6765239,
								"user": None if {"id": "public", "value": "public"} in currentRequest.get("preferences") else authorId,
								"channel": alert["channel"]
							})
							reference.delete()

						else:
							print("{}: price of {} ({}) hit {} {}".format(accountId, ticker.get("base"), payload.get("platform") if ticker.get("exchange") is None else ticker.get("exchange").get("name"), alert.get("levelText", alert["level"]), ticker.get("quote")))
						break

		except (KeyboardInterrupt, SystemExit): pass
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=f"{accountId}, {authorId}")
		socket.close()


if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	print("[Startup]: Alerts Server is in startup, running in {} mode.".format("production" if environ["PRODUCTION_MODE"] else "development"))

	if not environ["PRODUCTION_MODE"]: exit(0)
	alertsServer = AlertsServer()
	alertsServer.run()
