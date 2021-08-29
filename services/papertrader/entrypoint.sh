source /run/secrets/alpha-service/key
if [[ $PRODUCTION_MODE == "1" ]]
then
	python app/paper.py
else
	python -u app/paper.py
fi