#!/usr/bin/python
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class Topology(Topo):
    def __init__(self, bandwidth, **opts):
        Topo.__init__(self, **opts)

        r0 = self.addHost('r0', cls=LinuxRouter, ip='192.168.1.1/24')

        s1, s2 = [ self.addSwitch(s) for s in 's1', 's2' ]

        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '192.168.1.1/24'})
        self.addLink(s2, r0, intfName2='r0-eth2', params2={'ip': '192.168.2.1/24'})

        h1 = self.addHost('h1', ip='192.168.1.10/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.2.10/24', defaultRoute='via 192.168.2.1')

        for h, s in [(h1, s1), (h2, s2)]:
            self.addLink(h, s)


def testIt():
    topo = Topology(1)
    net = Mininet(topo)

    h1, h2, r0 = net.get('h1', 'h2', 'r0')

    #print "Running ntop"
    #r0.cmd('redis-server > /tmp/redis 2>&1 &')
    #r0.cmd('ntopng > /tmp/ntop 2>&1 &')

    #print "Running itgrecv"
    #h1.cmd("ITGRecv -a %s > /tmp/itgrecv 2>&1 &" % h1.IP())
    #print "Running itgsend"
    #h2.cmd("ITGSend -a %s -x hasil > /tmp/itgsend 2>&1 &" % h1.IP())

    dumpNodeConnections(net.hosts)
    net.pingAll()
    CLI(net)

    #h1.cmd('killall ITGRecv')
    #r0.cmd('killall ntopng')
    #r0.cmd('killall redis-server')
   
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testIt()