import time
from concurrent.futures import ThreadPoolExecutor

from scapy.all import *

from modules.SockManager import SocketManager


class Router:
    def __init__(self, addr, timeout, max_thread, verbose, guess, targets):
        self.addr = addr
        self.max_thread = max_thread
        self.verbose = verbose
        self.guess = guess
        self.targets = targets
        self.SocketManager = SocketManager(timeout)

    def start(self):
        while self.targets:
            futures = self.get_thread_pool()
            self.execute_pool_tasks(futures)

    def get_thread_pool(self):
        futures = {}
        with ThreadPoolExecutor(max_workers=self.max_thread) as pool:
            counter = 0
            while self.targets and counter < self.max_thread:
                target = self.targets.pop(0)
                future = pool.submit(self.work, self.addr, target)
                futures[future] = target
                counter += 1
        return futures

    def execute_pool_tasks(self, futures):
        for executor in futures:
            target = futures[executor]
            try:
                success, ping, proto = executor.result()
            except Exception as e:
                print(f'Problem occurred: {e}')
                raise
            else:
                self.print_result(success, ping, target, proto)

    def print_result(self, success, ping, target, proto):

        if success:
            protocol = self.define_protocol(proto)
            print(f'{target[0].upper()} {target[1]} {ping:.4f}ms {protocol}')
        else:
            print(f'{target[0].upper()} {target[1]} is closed')

    def work(self, addr, target):
        start_time = time.time()
        sent_packet, data = self.SocketManager.setup_connection(addr, target)
        ans = data[0]
        ping = time.time() - start_time
        if len(ans) != 0:
            r, s = ans[0]

            if str(s[1].flags).find('R') == -1:
                return True, ping, s.proto
        return False, ping, 0

    @staticmethod
    def define_protocol(proto):
        if proto == 6:
            return 'TCP'
        elif proto == 17:
            return 'UDP'
        elif proto == '1':
            return 'DNS'
