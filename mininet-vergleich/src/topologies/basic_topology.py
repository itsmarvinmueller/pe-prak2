from mininet.topo import Topo

class BasicTopology(Topo):
    def build(self, queue_size=100, bw=10, delay='5ms'):
        # Create four servers
        server1 = self.addHost('s1')
        server2 = self.addHost('s2')
        server3 = self.addHost('s3')
        server4 = self.addHost('s4')

        # Create a router
        router = self.addSwitch('r1')

        # Connect servers to the router with queue size, bandwidth, and delay
        linkopts = dict(max_queue_size=queue_size, bw=bw, delay=delay)
        self.addLink(server1, router, **linkopts)
        self.addLink(server2, router, **linkopts)
        self.addLink(server3, router, **linkopts)
        self.addLink(server4, router, **linkopts)

def SimulationTopo(queue_size=100, bw=10, delay='5ms'):
    return BasicTopology(queue_size=queue_size, bw=bw, delay=delay)