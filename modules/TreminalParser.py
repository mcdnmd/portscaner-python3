import argparse
import os
import socket


class TerminalParser:
    def extract_terminal_params(self):
        parser = argparse.ArgumentParser(description="Start a PORTSCAN utility")
        parser.add_argument(
            'addr',
            action='store',
            type=self.get_ip_addr,
            help='server domain or ip address')
        parser.add_argument(
            '--timeout',
            action='store',
            type=int,
            dest='timeout',
            default=2,
            help='response timeout (default 2s)'
        )
        parser.add_argument(
            '-j',
            '--num-threads',
            action='store',
            type=int,
            dest='max_threads',
            default=2 * os.cpu_count(),
            help='number of threads (default 2 * CPU)'
        )
        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            dest='verbose',
            help='verbose mode'
        )
        parser.add_argument(
            '-g',
            '--guess',
            action='store_true',
            dest='guess',
            help='application protocol definition'
        )
        parser.add_argument(
            'targets',
            nargs='+',
            type=self.get_protocol_and_ports_range
        )
        return parser.parse_args()

    @staticmethod
    def get_ip_addr(addr):
        return socket.gethostbyname(addr)

    def get_protocol_and_ports_range(self, string):
        tmp = string.split('/')
        method, unfiltered_ports = tmp[0], tmp[1].split(',')
        ports = {'single': [], 'multiple': []}
        for port in unfiltered_ports:
            tmp = port.split('-')
            start, end = tmp[0], tmp[len(tmp) - 1]
            if start == end:
                ports['single'].append((method, start))
            else:
                ports['multiple'].append((method, start, end))
        return ports

