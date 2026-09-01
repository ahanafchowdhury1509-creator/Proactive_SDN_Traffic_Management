from mininet.net import Mininet
from mininet.node import RemoteController
from Topology.multipath_top import MutliPathTopo
net=Mininet(topo=MutliPathTopo(),controller=RemoteController('c0',ip='127.0.0.1',port=6633))
net.start()
h1=net.get('h1')
h2=net.get('h2')
h2.cmd('iperf -s &')#Here At H2 Server running at the background
h1.cmd('iperf -c 10.0.0.2 -t 20 -b 1M')
h1.cmd('iperf -c 10.0.0.2 -t 20 -b 10M')
net.stop()