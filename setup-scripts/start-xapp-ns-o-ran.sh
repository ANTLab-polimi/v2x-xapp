#!/bin/bash
docker kill xapp-v2x-24
docker rm xapp-v2x-24
# docker rmi ef-xapp:latest

./setup-xapp.sh ns-o-ran

docker cp ../setup/xapp-v2x xapp-v2x-24:/home

docker exec -it xapp-v2x-24 bash
