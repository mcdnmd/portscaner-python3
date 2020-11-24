from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, TCP, UDP, ICMP


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
        return sr(packet, timeout=self.timeout, verbose=False)

    def scan_udp_port(self, addr, port):
        packet = IP(dst=addr)/UDP(dport=port)
        return sr(packet, timeout=self.timeout, verbose=False)

    def send_rst_request(self, addr, port):
        packet = IP(dst=addr)/TCP(dport=port, flags='R')
        return sr(packet, timeout=self.timeout, verbose=False)