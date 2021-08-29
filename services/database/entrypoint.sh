source /run/secrets/alpha-service/key
if [[ $PRODUCTION_MODE == "1" ]]
then
	python -u app/database.py
else
	python -u app/database.py
fi