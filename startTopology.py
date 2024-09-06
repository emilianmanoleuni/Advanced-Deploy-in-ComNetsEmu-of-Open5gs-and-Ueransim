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
#    r1 = net.addHost("r1", ip='192.168.0.1/24')
#    r2 = net.addHost('r2', ip='192.168.1.1/24')
    s1 = net.addSwitch("s1")
#    s2 = net.addSwitch("s2")

#    net.addLink(s1, r1, intfName1="s1-r1", intfName2="r1-s1", params1={'ip': '192.168.0.1/24'}, params2={'ip': '192.168.0.1/24'})
#    net.addLink(s2, r2, intfName1="s2-r2", intfName2="r2-s2", params1={'ip': '192.168.1.1/24'}, params2={'ip': '192.168.1.1/24'})
#    net.addLink(r1, r2, intfName1="r1-r2", intfName2="r2-r1", params1={'ip': '192.168.2.1/30'}, params2={'ip': '192.168.2.2/30'})
#    net.addLink(s1, r1, intfName1="s1-r1", intfName2="r1-s1")
#    net.addLink(s2, r2, intfName1="s2-r2", intfName2="r2-s2")
#    net.addLink(r1, r2, intfName1="r1-r2", intfName2="r2-r1")

#    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
#    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
#    r1.cmd('ip route add 192.168.1.0/24 via 192.168.2.2')
#    r2.cmd('ip route add 192.168.0.0/24 via 192.168.2.1')

    mongo = addComponent(net, "mongo", "192.168.0.2/24", s1)
    amf   = addComponent(net,   "amf", "192.168.0.3/24", s1)
    ausf  = addComponent(net,  "ausf", "192.168.0.4/24", s1)
    bsf   = addComponent(net,   "bsf", "192.168.0.5/24", s1)
    nrf   = addComponent(net,   "nrf", "192.168.0.6/24", s1)
    nssf  = addComponent(net,  "nssf", "192.168.0.7/24", s1)
    pcf   = addComponent(net,   "pcf", "192.168.0.8/24", s1)
    scp   = addComponent(net,   "scp", "192.168.0.9/24", s1)
    smf   = addComponent(net,   "smf", "192.168.0.10/24", s1)
    udm   = addComponent(net,   "udm", "192.168.0.11/24", s1)
    udr   = addComponent(net,   "udr", "192.168.0.12/24", s1)
    upf   = addComponent(net,   "upf", "192.168.0.13/24", s1)
    webui = addComponent(net, "webui", "192.168.0.14/24", s1)

#    gnb = addComponent(net, "gnb", "10.45.0.10/24")
#    ue = addComponent(net, "ue", "10.45.0.15/24")
    gnb = addComponent(net, "gnb", "192.168.0.20/24", s1)
    ue  = addComponent(net,  "ue", "192.168.0.30/24", s1)

    info("\n*** Starting network\n")
    net.start()
    setNetworkStatus("ready")

    CLI(net)

    net.stop()
