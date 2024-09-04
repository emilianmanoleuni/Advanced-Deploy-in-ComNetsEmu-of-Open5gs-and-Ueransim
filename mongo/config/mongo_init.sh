#!/bin/bash

echo "starting" > "$STATUS_FILE"

echo "----------------------------"
echo "INITIALIZING ${COMPONENT_NAME}"
echo "----------------------------"
echo "-->DB_URI: ${DB_URI}"
echo "----------------------------"
echo "INSTALLING DEPENDENCIES"

echo "installing" > "$STATUS_FILE"
#apt update && apt install net-tools && apt install iproute2 -y
echo "ready" > "$STATUS_FILE"

echo "DONE"
echo "----------------------------"

mongod --logpath /opt/open5gs/var/log/mongodb.log --logRotate reopen --logappend --bind_ip_all
