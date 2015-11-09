#!/usr/bin/python
import sys
from time import sleep

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
    bw = sys.argv[1]
    topo = Topology(int(bw))
    net = Mininet(topo, link=TCLink)
    net.start()
    h1, h2 = net.get('h1', 'h2')
    
    print "Start ITGRecv %s" % h2.IP()
    h2.cmd("redis-server > /tmp/redis 2>&1 &")
    sleep(5)
    h2.cmd("ntopng > /tmp/ntop 2>&1 &")
    sleep(5)
    h2.cmd("sar -u 1 60 > simple_ntop_cpu_%s &" % bw)
    h2.cmd("ITGRecv -a %s > /tmp/itgrecv 2>&1 &" % h2.IP())
    sleep(5)
    print "Start ITGSend"
    h1.cmd("ITGSend ditg-flow -x simple_ntop_%s > /tmp/itgsend 2>&1" % bw)

    h2.cmd('killall ITGRecv')
    h2.cmd('killall ntopng')
    h2.cmd('killall redis-server')
    h2.cmd('killall sar')
    #h1.cmd("ITGDec recv_log_file")

    net.stop()

if __name__ == '__main__':
    testIt()
