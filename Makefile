SHELL=/bin/bash

# DB
build_postgres:
	sudo docker build ./Postgres -t postgres

build_alerts:
	sudo docker build ./Alerts -t alerts

build:
	make build_postgres
	make build_alerts 

