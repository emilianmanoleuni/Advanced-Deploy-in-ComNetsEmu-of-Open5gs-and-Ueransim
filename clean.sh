#!/bin/bash

sudo mn -c

docker stop $(docker ps -aq)

docker container prune -f

if [ "$1" == "log" ]; then
    cd log && sudo rm *.log 
fi

sudo ip link delete s1-ue
sudo ip link delete s2-s3
sudo ip link delete s2-s1
sudo ip link delete gnb-s1
sudo ip link delete s1-gnb
sudo ip link delete s1-cp
sudo ip link delete gnb-s2
sudo ip link delete s2-gnb
sudo ip link delete s3-cp
sudo ip link delete s1-ue1
sudo ip link delete s1-ue2
sudo ip link delete s1-ue3
sudo ip link delete s2-upf_mec
sudo ip link delete s3-upf
sudo ip link delete s1-uegnb

sudo ip link delete s1-amf
sudo ip link delete s1-ausf
sudo ip link delete s1-bsf
sudo ip link delete s1-nrf
sudo ip link delete s1-nssf
sudo ip link delete s1-pcf
sudo ip link delete s1-scp
sudo ip link delete s1-smf
sudo ip link delete s1-udm
sudo ip link delete s1-udr

sudo ip link delete s1-r1
sudo ip link delete s2-r2
sudo ip link delete r1-r2

sudo ip link delete s1-mongo
sudo ip link delete s1-webui
