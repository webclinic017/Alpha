from os import environ
from signal import signal, SIGINT, SIGTERM
from time import time, sleep
from math import ceil
from zmq import Context, device, XREP, XREQ, QUEUE, ROUTER, NOBLOCK
from orjson import dumps
from traceback import format_exc
from threading import Thread, Lock

import stripe
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import DELETE_FIELD
from google.cloud.error_reporting import Client as ErrorReportingClient
from helpers.utils import Utils


database = FirestoreClient()
stripe.api_key = environ["STRIPE_KEY"]


class DatabaseHandler(object):
	accountsReady = False
	guildsReady = False
	usersReady = False

	accountProperties = {}
	guildProperties = {}
	accountIdMap = {}

	def __init__(self):
		self.isServiceAvailable = True
		self.isManager = False if len(environ["HOSTNAME"].split("-")) != 2 else environ["HOSTNAME"].split("-")[1] == "0"
		if self.isManager: print("[Startup]: This instance is a database manager")
		else: print("[Startup]: This instance is a slave")
		signal(SIGINT, self.exit_gracefully)
		signal(SIGTERM, self.exit_gracefully)

		self.accountLock = Lock()
		self.guildLock = Lock()

		self.logging = ErrorReportingClient(service="database")

		self.context = Context.instance()

		self.accountsLink = database.collection("accounts").on_snapshot(self.update_account_properties)
		while not self.accountsReady: sleep(1)
		self.discordPropertiesGuildsLink = database.collection("discord/properties/guilds").on_snapshot(self.update_guild_properties)
		while not self.guildsReady: sleep(1)
		self.discordPropertiesUnregisteredUsersLink = database.collection("discord/properties/users").on_snapshot(self.update_unregistered_users_properties)
		while not self.usersReady: sleep(1)

	def exit_gracefully(self):
		print("[Startup]: Database handler is exiting")
		self.isServiceAvailable = False

	def queue(self):
		try:
			frontend = self.context.socket(XREP)
			frontend.bind("tcp://*:6900")
			backend = self.context.socket(XREQ)
			backend.bind("tcp://*:6969")

			device(QUEUE, frontend, backend)
		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception()
		finally:
			pass
			frontend.close()
			backend.close()

	def run(self):
		socket = self.context.socket(ROUTER)
		socket.connect("tcp://localhost:6969")

		while self.isServiceAvailable:
			try:
				response = None
				message = socket.recv_multipart()
				if len(message) != 6: continue
				queue, origin, delimeter, service, timestamp, entityId = message
				if int(timestamp.decode()) < time() * 1000:
					print("Request received too late")
					continue

				if service == b"account_fetch":
					response = self.accountProperties.get(entityId.decode())
				elif service == b"guild_fetch":
					response = self.guildProperties.get(entityId.decode())
				elif service == b"account_keys":
					response = self.get_account_keys()
				elif service == b"guild_keys":
					response = self.get_guild_keys()
				elif service == b"account_match":
					response = self.accountIdMap.get(entityId.decode())
				elif service == b"account_status":
					response = self.accountsReady and self.usersReady
				elif service == b"guild_status":
					response = self.accountsReady and self.guildsReady

			except (KeyboardInterrupt, SystemExit): return
			except Exception:
				print(format_exc())
				if environ["PRODUCTION_MODE"]: self.logging.report_exception()
			finally:
				try: socket.send_multipart([queue, origin, delimeter, dumps(response)], flags=NOBLOCK)
				except: pass

		socket.close()

	def update_account_properties(self, settings, changes, timestamp):
		try:
			for change in changes:
				properties = change.document.to_dict()
				accountId = change.document.id

				# Safety
				for key in properties["apiKeys"]:
					properties["apiKeys"][key].pop("secret")
					properties["apiKeys"][key].pop("passphrase", None)

				with self.accountLock:
					if change.type.name in ["ADDED", "MODIFIED"]:
						self.accountProperties[accountId] = properties
						userId = properties["oauth"]["discord"].get("userId")
						if userId is not None:
							if userId in self.accountProperties:
								self.accountProperties.pop(userId)
							self.accountIdMap[userId] = accountId
							self.accountIdMap[accountId] = userId
					else:
						userId = self.accountProperties[accountId]["oauth"]["discord"].get("userId")
						if userId is not None:
							self.accountIdMap.pop(self.accountIdMap.get(accountId))
							self.accountIdMap.pop(accountId)
						self.accountProperties.pop(accountId)

			self.accountsReady = True

		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=accountId)

	def update_unregistered_users_properties(self, settings, changes, timestamp):
		try:
			for change in changes:
				properties = change.document.to_dict()
				accountId = change.document.id

				# Validation
				if self.isManager and self.unregistered_user_validation(accountId, properties): continue

				# Safety
				properties.pop("connection", None)
				properties.pop("trace", None)
				properties.pop("credit", None)
				if not properties: continue

				with self.accountLock:
					if change.type.name in ["ADDED", "MODIFIED"]:
						self.accountProperties[accountId] = properties
					else:
						self.accountProperties.pop(accountId)

			self.usersReady = True

		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=accountId)

	def update_guild_properties(self, settings, changes, timestamp):
		try:
			for change in changes:
				guildId = change.document.id
				properties = change.document.to_dict()

				# Validation
				if self.isManager and self.guild_validation(guildId, properties): continue

				with self.guildLock:
					if change.type.name in ["ADDED", "MODIFIED"]:
						self.guildProperties[guildId] = properties
					else:
						self.guildProperties.pop(guildId, None)

			self.guildsReady = True

		except Exception:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=guildId)

	def get_account_keys(self):
		response = {}
		with self.accountLock:
			for account, properties in self.accountProperties.items():
				response[account] = properties.get("oauth", {}).get("discord", {}).get("userId")
		return response

	def get_guild_keys(self):
		response = {}
		with self.guildLock:
			for guildId, properties in self.guildProperties.items():
				if properties.get("stale", {}).get("timestamp", time()) <= time() - 86400:
					database.document("discord/properties/guilds/{}".format(guildId)).set({"stale": DELETE_FIELD}, merge=True)
				response[guildId] = properties.get("settings", {}).get("setup", {}).get("connection")
		return response

	def unregistered_user_validation(self, accountId, properties):
		try:
			if "commandPresets" in properties and len(properties["commandPresets"]) == 0:
				properties.pop("commandPresets")
				database.document("discord/properties/users/{}".format(accountId)).set(properties)
				return True
			if not properties:
				database.document("discord/properties/users/{}".format(accountId)).delete()
				return True
		except:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=accountId)
		return False

	def guild_validation(self, guildId, properties):
		try:
			if "addons" not in properties or "settings" not in properties:
				database.document("discord/properties/guilds/{}".format(guildId)).set(Utils.create_guild_settings(properties))
				return True
			if "stale" in properties:
				if properties["stale"].get("count", 0) >= 96:
					database.document("discord/properties/guilds/{}".format(guildId)).delete()
					return True
				elif properties["stale"].get("timestamp", time()) <= time() - 86400:
					database.document("discord/properties/guilds/{}".format(guildId)).set({"stale": DELETE_FIELD}, merge=True)
					return True
			if properties["addons"]["satellites"]["enabled"]:
				addedSatellites = properties["addons"]["satellites"].get("added", [])
				satelliteCount = len(addedSatellites)
				if satelliteCount > properties["addons"]["satellites"].get("count", 0):
					accountProperties = self.accountProperties.get(properties["addons"]["satellites"].get("connection"))
					if accountProperties["customer"]["personalSubscription"].get("subscription") is not None:
						if environ["PRODUCTION_MODE"]:
							subscription = stripe.Subscription.retrieve(accountProperties["customer"]["personalSubscription"]["subscription"])
							cycleRatio = (subscription["current_period_end"] - time()) / (subscription["current_period_end"] - subscription["current_period_start"])
							quantity = int(ceil((satelliteCount - properties["addons"]["satellites"].get("count", 0)) * 20 * cycleRatio))
							stripe.SubscriptionItem.create_usage_record(subscription["items"]["data"][0]["id"], quantity=quantity, timestamp=int(time()), action="increment")
							database.document("discord/properties/guilds/{}".format(guildId)).set({"addons": {"satellites": {"enabled": True, "count": satelliteCount}}}, merge=True)
							return True
						else:
							print("{}: {} satellites".format(guildId, satelliteCount))
			elif properties["addons"]["satellites"].get("count") is not None:
				properties["addons"]["satellites"].pop("count", None)
				properties["addons"]["satellites"].pop("added", None)
				database.document("discord/properties/guilds/{}".format(guildId)).set(properties)
				return True

		except:
			print(format_exc())
			if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=guildId)
		return False


if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	print("[Startup]: Database handler Server is in startup, running in {} mode.".format("production" if environ["PRODUCTION_MODE"] else "development"))
	databaseHandler = DatabaseHandler()
	print("[Startup]: Database handler is ready")

	processingThreads = []
	for i in range(3):
		p = Thread(target=databaseHandler.run)
		p.start()
		processingThreads.append(p)

	print("[Startup]: Database handler is online")
	databaseHandler.queue()
	