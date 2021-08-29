from time import time

from pycoingecko import CoinGeckoAPI
from markdownify import markdownify

from components.abstract import AbstractProvider


class CoinGecko(AbstractProvider):
	connection = CoinGeckoAPI()

	@classmethod
	def request_details(cls, request):
		ticker = request.get("ticker")

		try:
			assetData = CoinGecko.connection.get_coin_by_id(id=ticker.get("symbol"), localization="false", tickers=False, market_data=True, community_data=True, developer_data=True)
			historicData = CoinGecko.connection.get_coin_ohlc_by_id(id=ticker.get("symbol"), vs_currency="usd", days=365)
		except:
			return [{}, ""]

		description = markdownify(assetData["description"].get("en", "No description"))
		descriptionParagraphs = description.split("\r\n\r\n")
		textLength = [len(descriptionParagraphs[0])]
		for i in range(1, len(descriptionParagraphs)):
			nextLength = textLength[-1] + len(descriptionParagraphs[i])
			if nextLength > 500 and textLength[-1] > 300 or nextLength > 1900: break
			textLength.append(nextLength)
		description = "\n".join(descriptionParagraphs[:len(textLength)])[:] + "\n[Read more on CoinGecko](https://www.coingecko.com/coins/{})".format(ticker.get("symbol"))

		highs = [e[2] for e in historicData]
		lows = [e[3] for e in historicData]

		payload = {
			"name": "{} ({})".format(assetData["name"], ticker.get("base")),
			"description": description,
			"rank": assetData["market_data"]["market_cap_rank"],
			"supply": {},
			"score": {
				"developer": assetData["developer_score"],
				"community": assetData["community_score"],
				"liquidity": assetData["liquidity_score"],
				"public interest": assetData["public_interest_score"]
			},
			"price": {
				"current": assetData["market_data"]["current_price"].get("usd"),
				"ath": assetData["market_data"]["ath"].get("usd"),
				"atl": assetData["market_data"]["atl"].get("usd")
			},
			"change": {
				"past day": assetData["market_data"]["price_change_percentage_24h_in_currency"].get("usd"),
				"past month": assetData["market_data"]["price_change_percentage_30d_in_currency"].get("usd"),
				"past year": assetData["market_data"]["price_change_percentage_1y_in_currency"].get("usd")
			},
			"sourceText": "Data from CoinGecko",
			"platform": "CoinGecko",
		}

		if assetData["image"]["large"].startswith("http"): payload["image"] = assetData["image"]["large"]
		if assetData["links"]["homepage"][0] != "": payload["url"] = assetData["links"]["homepage"][0].replace(" ", "") if assetData["links"]["homepage"][0].replace(" ", "").startswith("http") else "https://" + assetData["links"]["homepage"][0].replace(" ", "")
		if assetData["market_data"]["total_volume"] is not None: payload["volume"] = assetData["market_data"]["total_volume"].get("usd")
		if assetData["market_data"]["market_cap"] is not None: payload["marketcap"] = assetData["market_data"]["market_cap"].get("usd")
		if assetData["market_data"]["total_supply"] is not None: payload["supply"]["total"] = assetData["market_data"]["total_supply"]
		if assetData["market_data"]["circulating_supply"] is not None: payload["supply"]["circulating"] = assetData["market_data"]["circulating_supply"]
		if len(highs) != 0: payload["price"]["1y high"] = max(highs)
		if len(lows) != 0: payload["price"]["1y low"] = min(lows)

		return [payload, ""]