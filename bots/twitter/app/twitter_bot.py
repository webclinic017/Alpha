from os import environ
import twitter


def main():
	consumer_key = environ["TWITTER_CONSUMER_KEY"]
	consumer_secret = environ["TWITTER_CONSUMER_SECRET"]
	access_key = environ["TWITTER_API_KEY"]
	access_secret = environ["TWITTER_API_SECRET"]

	message = "Hellow World"

	twitterApi = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_key, access_token_secret=access_secret, input_encoding="utf-8")
	# status = twitterApi.PostUpdate(message)

	# print("{0} just posted: {1}".format(status.user.name, status.text))

if __name__ == "__main__":
	main()