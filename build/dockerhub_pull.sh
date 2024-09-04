#!/bin/bash
docker pull gradiant/open5gs:2.7.1
docker pull gradiant/open5gs-webui:2.7.1
docker pull gradiant/ueransim:3.2.6
docker pull mongo:latest

docker tag gradiant/open5gs:2.7.1  open5gs_image
docker tag gradiant/open5gs-webui:2.7.1  open5gs_webui_image
docker tag gradiant/ueransim:3.2.6  ueransim_image
docker tag mongo:latest mongo_image
