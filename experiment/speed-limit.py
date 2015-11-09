#!/usr/bin/python
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

class Topology(Topo):
    def __init__(self, bandwidth, **opts):
        Topo.__init__(self, **opts)

        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1, s1, bw=bandwidth)
        self.addLink(h2, s1, bw=bandwidth)

def testIt():
    topo = Topology(int(sys.argv[1]))
    net = Mininet(topo, link=TCLink)
    net.start()
    h1, h2 = net.get('h1', 'h2')
    net.iperf((h1,h2))
    net.stop()

if __name__ == '__main__':
    testIt()
