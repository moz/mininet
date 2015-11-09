#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet 
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI 
from mininet.util import dumpNodeConnections

class NetworkTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        h1 = self.addHost('h1', ip='192.168.1.1/24')
        h2 = self.addHost('h2', ip='192.168.1.2/24')

        s1 = self.addSwitch('s1')

        self.addLink(h1, s1)
        self.addLink(h2, s1)

def run():
    topo = NetworkTopo()
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
