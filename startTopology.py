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

from CreateComponents5g import addComponent, createLink, setNetworkStatus


if __name__ == "__main__":

    setNetworkStatus("starting")

    setLogLevel("info")

    net = Containernet(controller=Controller, link=TCLink)

    net.addController("c0")
    s1 = net.addSwitch("s1")

    mongo = addComponent(net, "mongo", "10.0.0.2/24", s1)
    amf   = addComponent(net,   "amf", "10.0.0.3/24", s1)
    ausf  = addComponent(net,  "ausf", "10.0.0.4/24", s1)
    bsf   = addComponent(net,   "bsf", "10.0.0.5/24", s1)
    nrf   = addComponent(net,   "nrf", "10.0.0.6/24", s1)
    nssf  = addComponent(net,  "nssf", "10.0.0.7/24", s1)
    pcf   = addComponent(net,   "pcf", "10.0.0.8/24", s1)
    scp   = addComponent(net,   "scp", "10.0.0.9/24", s1)
    smf   = addComponent(net,   "smf", "10.0.0.10/24", s1)
    udm   = addComponent(net,   "udm", "10.0.0.11/24", s1)
    udr   = addComponent(net,   "udr", "10.0.0.12/24", s1)
    upf   = addComponent(net,   "upf", "10.0.0.13/24", s1)
    webui = addComponent(net, "webui", "10.0.0.14/24", s1)

    gnb = addComponent(net, "gnb", "10.0.0.20/24", s1)
    ue  = addComponent(net,  "ue", "10.0.0.21/24", s1)

    info("\n*** Starting network\n")
    net.start()
    setNetworkStatus("ready")

    CLI(net)

    net.stop()
