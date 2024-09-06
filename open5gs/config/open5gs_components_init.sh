#!/bin/bash

LOG_DIR="/opt/open5gs/var/log"

STATUS_FILE_NETWORK="${STATUS_DIR_PATH}/network_status.txt"

echo "starting" > "$STATUS_FILE"

echo "----------------------------"
echo "INITIALIZING ${COMPONENT_NAME}"
echo "----------------------------"
echo "-->DB_URI: ${DB_URI}"
echo "----------------------------"
echo "INSTALLING DEPENDENCIES"

echo "installing" > "$STATUS_FILE"
#apt-get update && apt-get install -y gettext


echo "--> Copy ${COMPONENT_NAME}.yaml"
envsubst < /opt/open5gs/etc/open5gs/config/$COMPONENT_NAME.yaml > /opt/open5gs/etc/open5gs/$COMPONENT_NAME.yaml

sleep 1

echo "ready" > "$STATUS_FILE"

echo "DONE"
echo "----------------------------"

echo "Starting service >>"

waitForNetwork() {
    local status_file=$STATUS_FILE_NETWORK
    local expected_status="ready"

    while true; do
        if [ -f "$status_file" ]; then
            STATUS=$(cat "$status_file")
            if [ "$STATUS" == "$expected_status" ]; then
                break
            fi
        else
            echo "Status file can't be found: $status_file"
            sleep 1
        fi
    done
    sleep 1
}

case "$COMPONENT_NAME" in
    "amf")
        open5gs-amfd
        ;;
    "ausf")
        open5gs-ausfd
        ;;
    "bsf")
        open5gs-bsfd
        ;;
    "nrf")
        open5gs-nrfd
        ;;
    "nssf")
        open5gs-nssfd
        ;;
    "pcf")
        waitForNetwork
        open5gs-pcfd
        ;;
    "scp")
        open5gs-scpd
        ;;
    "smf")
        open5gs-smfd
        ;;
    "udm")
        open5gs-udmd
        ;;
    "udr")
        waitForNetwork
        open5gs-udrd
        ;;
    "upf")
        ip tuntap add name ogstun mode tun
        ip addr add 10.45.0.1/16 dev ogstun
        ip link set ogstun up
        iptables -t nat -A POSTROUTING -s 10.45.0.1/16 ! -o ogstun -j MASQUERADE

        iperf3 -B 10.45.0.1 -s -fm &

        open5gs-upfd
        ;;
    *)
    echo "Unknowkn component: ${COMPONENT_NAME}"
    exit 1
    ;;
esac
