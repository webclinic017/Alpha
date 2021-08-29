source /run/secrets/alpha-service/key

# npm install
yarn install

ulimit -n 8192

if [[ $PRODUCTION_MODE == "1" ]]
then
	node app/serum_server.js
else
	node app/serum_server.js
fi