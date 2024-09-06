#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import mongo
import time
import subprocess
from dotenv import load_dotenv

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

OPEN5GS_IMAGE = "open5gs_modified_image"
OPEN5GS_WEBUI_IMAGE = "open5gs_webui_modified_image"

UERANSIM_IMAGE = "ueransim_modified_image"

MONGODB_IMAGE = "mongo_modified_image"

AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

setLogLevel("info")

prj_folder = "/home/vagrant/comnetsemu/app/Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim"

VOLUMES = {
    prj_folder + "/log": {
        "bind": "/opt/open5gs/var/log/",
        "mode": "rw",
    },
    prj_folder + "/mongo/config": {
        "bind": "/opt/mongo/",
        "mode": "rw",
    },
    prj_folder + "/open5gs/config": {
        "bind": "/opt/open5gs/etc/open5gs/config",
        "mode": "rw",
    },
    prj_folder + "/statuses": {
        "bind": "/opt/statuses",
        "mode": "rw",
    },
    prj_folder + "/ueransim/scripts": {
        "bind": "/opt/ueransim",
        "mode": "rw",
    },
    "/etc/timezone": {
        "bind": "/etc/timezone",
        "mode": "ro",
    },
    "/etc/localtime": {
        "bind": "/etc/localtime",
        "mode": "ro",
    }
}

load_dotenv()

env_vars = {
    "DB_URI": os.getenv("DB_URI"),
    "MONGO_IP": os.getenv("MONGO_IP"),
    "AMF_IP": os.getenv("AMF_IP"),
    "AUSF_IP": os.getenv("AUSF_IP"),
    "BSF_IP": os.getenv("BSF_IP"),
    "NRF_IP": os.getenv("NRF_IP"),
    "NSSF_IP": os.getenv("NSSF_IP"),
    "PCF_IP": os.getenv("PCF_IP"),
    "SCP_IP": os.getenv("SCP_IP"),
    "SMF_IP": os.getenv("SMF_IP"),
    "UDM_IP": os.getenv("UDM_IP"),
    "UDR_IP": os.getenv("UDR_IP"),
    "UPF_IP": os.getenv("UPF_IP"),
    "WEBUI_IP": os.getenv("WEBUI_IP")
}

DELAY_CORE_NETWORK = "1ms"
BW_CORE_NETWORK = 500

DELAY_EDGE_NETWORK = "5ms"
BW_EDGE_NETWORK = 750

########################################################################
#                                                                      #
#                            ADD COMPONENT                             #
#                                                                      #
########################################################################

def addComponent(net, name, ip_value, switch):

    info(f"\n--> Adding {name} IP: {ip_value}\n")

    #Define interface name instead of eth0
    intfName = f"{name}-{switch.name}"

    #Define name of the component to env variable
    component_env = {
        "COMPONENT_NAME": name,
        "INTERFACE_NAME": intfName,
        "STATUS_DIR_PATH": "/opt/statuses/",
        "STATUS_FILE": "/opt/statuses/" + name + "_status.txt"
    }

    #Add IPs of the other components for yamls
    if name != "mongo":
        for key, value in env_vars.items():
            component_env[key] = value
        #Mongo doesn't need them
#        if key != "MONGO_IP":


    ##################### MONGO #####################

    if name == "mongo":
        #DB name
        init_db_env = component_env
        init_db_env.update({
            "MONGO_INITDB_DATABASE": "open5gs"
        })

        component = net.addDockerHost(
            name,
            dimage=MONGODB_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/mongo/mongo_init.sh",
            docker_args={
                "environment": init_db_env,
                "volumes": VOLUMES,
            },
        )

        time.sleep(1)

        waitToBeReady(name)

        createLink(net, ip_value, component, switch, BW_CORE_NETWORK, DELAY_CORE_NETWORK)


    #################### UERANSIM ####################

    elif name == "gnb":
        init_gnb_env = component_env
        init_gnb_env.update({
#            "AMF_HOSTNAME": os.getenv("AMF_IP"),
            "AMF_IP": os.getenv("AMF_IP"),
            "GNB_IP": os.getenv("GNB_IP"),
            "GNB_HOSTNAME": os.getenv("GNB_IP"),
            "RADIO_BIND_IP": os.getenv("GNB_IP"),
            "N2_BIND_IP": os.getenv("GNB_IP"),
            "N3_BIND_IP": os.getenv("GNB_IP"),
#            "GNB_HOSTNAME": "ueransim_gnb",
            "TAC": '1',
            #"MCC": '999', Can't be used, private are above
            #"MNC": '70',
            "MCC": '001',
            "MNC": '01',
            "SST": '1',
            "SD": '0xffffff'
        })

        component = net.addDockerHost(
            name,
            dimage=UERANSIM_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/ueransim/init_gnb.sh",
            docker_args={
                "environment": component_env,
                "volumes": VOLUMES,
            },
        )

        waitToBeReady(name)

        createLink(net, ip_value, component, switch, BW_EDGE_NETWORK, DELAY_EDGE_NETWORK)


    elif name == "ue":
        init_ue_env = component_env
        init_ue_env.update({
            "GNB_HOSTNAME": os.getenv("GNB_IP"),
            "GNB_IP": os.getenv("GNB_IP"),
            "APN": 'internet',
            "MSISDN": '0000000001',
            #"MCC": '999',
            #"MNC": '70',
            "MCC": '001',
            "MNC": '01',
            "KEY": '465B5CE8B199B49FAA5F0A2EE238A6BC',
            "OP_TYPE": "OPC",
            "OP": 'E8ED289DEBA952E4283B54E88E6183CA',
            "SST": '1',
            "SD": '0xffffff'
        })

        component = net.addDockerHost(
            name,
            dimage=UERANSIM_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/ueransim/init_ue.sh",
            docker_args={
                "environment": component_env,
                 "volumes": VOLUMES,
            },
        )

        waitToBeReady(name)

        createLink(net, ip_value, component, switch, BW_EDGE_NETWORK, DELAY_EDGE_NETWORK)


    #################### OPEN5GS ####################

    elif name == "amf":
        component = net.addDockerHost(
            name,
            dimage=OPEN5GS_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/open5gs/etc/open5gs/config/open5gs_components_init.sh",
            docker_args={
               "ports": {
                   "38412/tcp": 38412
                },
                "environment": component_env,
                "volumes": VOLUMES,
            },
        )

        createLink(net, ip_value, component, switch, BW_CORE_NETWORK, DELAY_CORE_NETWORK)

    elif name == "upf":
        component = net.addDockerHost(
            name,
            dimage=OPEN5GS_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/open5gs/etc/open5gs/config/open5gs_components_init.sh",
            docker_args={
               "ports": {
                   "2152/tcp": 2152
                },
                "environment": component_env,
                "volumes": VOLUMES,
            },
        )

        createLink(net, ip_value, component, switch, BW_CORE_NETWORK, DELAY_CORE_NETWORK)

    elif name == "webui":
        init_webui_env = {
            "NODE_ENV": "dev",
            "DB_URI": os.getenv("DB_URI")
        }

        component = net.addDockerHost(
            name,
            dimage=OPEN5GS_WEBUI_IMAGE,
            ip=ip_value,
            #dcmd="",
            docker_args={
               "ports": {
                   "9999/tcp": 9999,
               },
               "environment": init_webui_env,
               "volumes": VOLUMES,
            },
        )

        createLink(net, ip_value, component, switch, BW_CORE_NETWORK, DELAY_CORE_NETWORK)

    else:
        component = net.addDockerHost(
            name,
            dimage=OPEN5GS_IMAGE,
            ip=ip_value,
            dcmd="bash /opt/open5gs/etc/open5gs/config/open5gs_components_init.sh",
            docker_args={
                "environment": component_env,
                "volumes": VOLUMES,
            },
        )

        createLink(net, ip_value, component, switch, BW_CORE_NETWORK, DELAY_CORE_NETWORK)

    return component


########################################################################
#                                                                      #
#                          COMMON FUNCTIONS                            #
#                                                                      #
########################################################################

# node1 component - node2 switch
def createLink(net, ip, node1, node2, bw, delay):
    intfName1 = f"{node1.name}-{node2.name}"
    intfName2 = f"{node2.name}-{node1.name}"
    params1={'ip': ip}
    info(f"*** Creating link between {node1.name} and {node2.name} with interfaces {intfName1} and {intfName2}\n")
    net.addLink(node1, node2, bw=bw, delay=delay, intfName1=intfName1, intfName2=intfName2, params1=params1)

    return intfName1

def waitToBeReady(componentName):
    while True:
        try:
            with open(prj_folder + "/statuses/" + componentName +"_status.txt", 'r') as file:
                status = file.read().strip()
            if status == "ready":
                break

        except FileNotFoundError:
            print(f"Status file {componentName} not found.")

def setNetworkStatus(status):
    if status == "starting":
        print(f"-------------------------------------------------------------")
        print(f"|                                                           |")
        print(f"|   Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim   |")
        print(f"|                         v 1.0                             |")
        print(f"|                                                           |")
        print(f"-------------------------------------------------------------")

    try:
        with open(prj_folder + "/statuses/network_status.txt", 'w') as file:
            file.write(status + "\n")

    except Exception as e:
        print(f"An error occurred while writing to the status file: {e}")
