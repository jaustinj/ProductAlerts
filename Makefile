SHELL=/bin/bash

# # SIXPM
# build_sixpm_ingester:
# 	cp -r ./tools ./ingesters/SixPmIngester
# 	cp ./config/config.py ./ingesters/SixPmIngester
# 	sudo docker build ./ingesters/SixPmIngester -t sixpm_ingester

# build_sixpm_alerts:
# 	cp -r ./tools ./alert_services/SixPmAlerts
# 	cp ./config/config.py ./alert_services/SixPmAlerts
# 	sudo docker build ./alert_services/SixPmAlerts -t sixpm_alerts 

# # SIERRA TRADING POST
# build_sierra_ingester:
# 	cp -r ./tools ./ingesters/SierraIngester
# 	cp ./config/config.py ./ingesters/SierraIngester
# 	sudo docker build ./ingesters/SierraIngester -t sierra_ingester

# build_sierra_alerts:
# 	cp -r ./tools ./alert_services/SierraAlerts
# 	cp ./config/config.py ./alert_services/SierraAlerts
# 	sudo docker build ./alert_services/SierraAlerts -t sierra_alerts 

# DB
build_postgres:
	sudo docker build ./postgres -t productalertsdb

build_sierra:
	sudo docker build ./alerts -t sierra 

build:
	make build_postgres
	make build_sierra 

# # Push new code to docker images, but don't reimage db
# push:
# 	make build_sixpm_ingester
# 	make build_sixpm_alerts
# 	make build_sierra_ingester
# 	make build_sierra_alerts

# # build all images
# build:
# 	make build_sixpm_ingester
# 	make build_sixpm_alerts
# 	make build_sierra_ingester
# 	make build_sierra_alerts
# 	make build_postgres

# python:
# 	( \
# 	virtualenv --python=python3 env; \
# 	source env/bin/activate; \
# 	pip install -r requirements.txt; \
# 	)