from os import environ
from time import time

from iexfinance.stocks import Stock

from components.abstract import AbstractProvider


class IEXC(AbstractProvider):
	@classmethod
	def request_details(cls, request):
		ticker = request.get("ticker")

		try:
			stock = Stock(ticker.get("id"), token=environ["IEXC_KEY"])
			companyData = stock.get_company().loc[ticker.get("id")]
			rawData = stock.get_quote().loc[ticker.get("id")]
			historicData = stock.get_historical_prices(range="1y")
		except:
			return [{}, ""]

		try: stockLogoThumbnail = stock.get_logo().loc[ticker.get("id")]["url"]
		except: stockLogoThumbnail = None

		payload = {
			"name": companyData["symbol"] if companyData["companyName"] is None else "{} ({})".format(companyData["companyName"], companyData["symbol"]),
			"info": {
				"employees": companyData["employees"]
			},
			"price": {
				"current": rawData["delayedPrice"] if rawData["latestPrice"] is None else rawData["latestPrice"],
				"1y high": historicData.high.max(),
				"1y low": historicData.low.min(),
				"per": rawData["peRatio"]
			},
			"change": {
				"past day": ((historicData.close[-1] / historicData.close[-2] - 1) * 100 if historicData.shape[0] >= 2 and historicData.close[-2] != 0 else None) if rawData["changePercent"] is None else rawData["changePercent"] * 100,
				"past month": (historicData.close[-1] / historicData.close[-21] - 1) * 100 if historicData.shape[0] >= 21 and historicData.close[-21] != 0 else None,
				"past year": (historicData.close[-1] / historicData.close[0] - 1) * 100 if historicData.shape[0] >= 200 and historicData.close[0] != 0 else None
			},
			"sourceText": "Data provided by IEX Cloud",
			"platform": "IEXC",
		}

		if stockLogoThumbnail is not None: payload["image"] = stockLogoThumbnail
		if companyData["description"] is not None: payload["description"] = companyData["description"]
		if companyData["industry"] is not None and companyData["industry"] != "": payload["industry"] = companyData["industry"]
		if "marketCap" in rawData: payload["marketcap"] = rawData["marketCap"]
		if companyData["website"] is not None and companyData["website"] != "": payload["url"] = companyData["website"] if companyData["website"].startswith("http") else "https://" + companyData["website"]
		if companyData["country"] is not None: payload["info"]["location"] = "{}{}, {}, {}, {}".format(companyData["address"], "" if companyData["address2"] is None else ", " + companyData["address2"], companyData["city"], companyData["state"], companyData["country"])

		return [payload, ""]