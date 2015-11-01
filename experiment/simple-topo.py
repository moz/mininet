#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SingleSwitch(Topo):
    def build(self, n=2):
        switch = self.addSwitch("s1")

        for h in range(n):
            host = self.addHost('h%s' % (h+1))
            self.addLink(host, switch)

def testIt():
    topo = SingleSwitch()
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testIt()
