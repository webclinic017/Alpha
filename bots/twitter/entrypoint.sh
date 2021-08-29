source /run/secrets/alpha-service/key
if [[ $PRODUCTION_MODE == "1" ]]
then
	python app/twitter_bot.py
else
	python -u app/twitter_bot.py
fi