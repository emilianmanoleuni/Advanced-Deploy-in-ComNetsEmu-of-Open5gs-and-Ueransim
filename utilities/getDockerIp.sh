#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

CONTAINER_NAME=$1

DOCKER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME")

if [ -z "$DOCKER_IP" ]; then
    echo "No IP address found for container: $CONTAINER_NAME"
    exit 1
fi

echo "IP address of $CONTAINER_NAME: $DOCKER_IP"
