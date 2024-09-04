#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import mongo
import time

from dotenv import load_dotenv

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

from CreateComponents5g import addComponent, setNetworkStatus


if __name__ == "__main__":
    setNetworkStatus("starting")
#    makeStarting()

    setLogLevel("info")

    net = Containernet(controller=Controller, link=TCLink)

    net.addController("c0")
    s1 = net.addSwitch("s1")
#    s2 = net.addSwitch("s2")


    mongo = addComponent(net, "mongo", "192.168.1.110/24", s1)
    amf   = addComponent(net,   "amf", "192.168.1.111/24", s1)
    ausf  = addComponent(net,  "ausf", "192.168.1.112/24", s1)
    bsf   = addComponent(net,   "bsf", "192.168.1.113/24", s1)
    nrf   = addComponent(net,   "nrf", "192.168.1.114/24", s1)
    nssf  = addComponent(net,  "nssf", "192.168.1.115/24", s1)
    pcf   = addComponent(net,   "pcf", "192.168.1.116/24", s1)
    scp   = addComponent(net,   "scp", "192.168.1.117/24", s1)
    smf   = addComponent(net,   "smf", "192.168.1.118/24", s1)
    udm   = addComponent(net,   "udm", "192.168.1.119/24", s1)
    udr   = addComponent(net,   "udr", "192.168.1.120/24", s1)
    upf   = addComponent(net,   "upf", "192.168.1.121/24", s1)
    webui = addComponent(net, "webui", "192.168.1.122/24", s1)

#    print("-------------------------------\n")
#    print("Waiting to fully deploy Open5gs\n")
#    print("-------------------------------\n")
#    time.sleep(30)
#    while True:
#        user_input = input("Please type 'yes' to continue: ")
#        if user_input.lower() == "yes":
#            break
#        else:
#            print("Invalid input. Please type 'yes' to continue.")

#    gnb = addComponent(net, "gnb", "10.45.0.10/24")
#    ue = addComponent(net, "ue", "10.45.0.15/24")
    ueransim_gnb = addComponent(net, "ueransim_gnb", "192.168.1.130/24", s1)
    ueransim_ue = addComponent(net, "ueransim_ue", "192.168.1.131/24", s1)
#    srsran_gnb = addComponent(net, "srsran_gnb", "10.45.0.10/24", s1)
#    srsran_ue = addComponent(net, "srsran_ue", "10.45.0.15/24", s1)

    info("\n*** Starting network\n")
    net.start()
    setNetworkStatus("ready")

    CLI(net)

    net.stop()
