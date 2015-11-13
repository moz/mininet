#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet 
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI 
from mininet.util import dumpNodeConnections
from mininet.nodelib import NAT

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class Nat(NAT):
    def config(self, **params):
        super(Nat, self).config(**params)
        self.cmd('route add -net 192.168.0.0/16 gw 192.168.3.2')

class NetworkTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        r0 = self.addNode('r0', cls=LinuxRouter, ip='192.168.1.1/24', defaultRoute='via 192.168.3.1')
        s1, s2, s3 = [ self.addSwitch(s) for s in 's1', 's2', 's3' ]

        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '192.168.1.1/24'})
        self.addLink(s2, r0, intfName2='r0-eth2', params2={'ip': '192.168.2.1/24'})
        self.addLink(s3, r0, intfName2='r0-eth3', params2={'ip': '192.168.3.2/24'})

        nat = self.addNode('nat', cls=Nat, ip='192.168.3.1/24', subnet='192.168.0.0/16', inNamespace=False)
        self.addLink(nat, s3)

        h1 = self.addHost('h1', ip='192.168.1.2/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.2.2/24', defaultRoute='via 192.168.2.1')

        self.addLink(h1, s1)
        self.addLink(h2, s2)


def set_limit(host, eth, bw):
    host.cmd('ethtool -K %s gro off' % eth)
    host.cmd('tc qdisc add dev %s root handle 5:0 htb default 1' % eth)
    host.cmd('tc class add dev %s parent 5:0 classid 5:1 htb rate %dMbit burst 15k' % (eth, bw))

def run():
    topo = NetworkTopo()
    net = Mininet(topo)

    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()

    r0 = net.get('r0')

    limit = 50 #<< set limit disini dalam Mbit
    set_limit(r0, 'r0-eth1', limit)
    set_limit(r0, 'r0-eth2', limit)

    r0.cmd('redis-server > /tmp/redis-log 2>&1 &')
    r0.cmd('ntopng > /tmp/ntop-log 2>&1 &')

    CLI(net)

    r0.cmd('killall ntopng')
    r0.cmd('killall redis-server')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

