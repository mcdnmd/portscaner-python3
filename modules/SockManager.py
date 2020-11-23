from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP


class SocketManager:
    def __init__(self, timeout):
        self.timeout = timeout

    def setup_connection(self, addr, target):
        method = target[0]
        port = int(target[1])
        if method == 'tcp':
            return self.scan_tcp_port(addr, port)
        else:
            return self.scan_udp_port(addr, port)

    def scan_tcp_port(self, addr, port):
        packet = IP(dst=addr)/TCP(dport=port, flags='S')
        return packet, sr(packet, timeout=self.timeout, verbose=False)

    def scan_udp_port(self, addr, port):
        packet = IP(dst=addr)/UDP(dport=port)
        return packet, sr(packet, timeout=self.timeout, verbose=False)
