SHELL=/bin/bash

# DB
build_postgres:
	sudo docker build ./Postgres -t postgres

build_alerts:
	sudo docker build ./Alerts -t alerts

build:
	make build_postgres
	make build_alerts 

wipe_all_docker_on_your_whole_computer_warning:
	sudo docker stop $$(sudo docker ps -aq)
	sudo docker rm -f $$(sudo docker ps -aq)
	sudo docker rmi -f $$(sudo docker images -q)
	sudo docker volume rm $$(sudo docker volume ls -q)