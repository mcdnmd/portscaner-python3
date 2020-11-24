import time
from concurrent.futures import ThreadPoolExecutor

from scapy.all import *
from scapy.layers.inet import UDP, TCP, ICMP

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
                success, ping = executor.result()
            except Exception as e:
                print(f'Problem occurred: {e}')
                raise
            else:
                self.print_result(success, ping, target)

    def print_result(self, success, ping, target):

        if success:
            print(f'{target[0].upper()} {target[1]} {ping:.4f}ms')
        else:
            print(f'{target[0].upper()} {target[1]} is closed')

    def work(self, addr, target):
        start_time = time.time()
        data = self.SocketManager.setup_connection(addr, target)
        ans = data[0]
        ping = time.time() - start_time
        if len(ans) != 0:
            r, s = ans[0]
            if s.haslayer(TCP):
                if str(s.getlayer(TCP).flags).find('R') == -1:
                    self.SocketManager.send_rst_request(addr, int(target[1]))
                    return True, ping
            else:
                if s.haslayer(UDP):
                    return True, ping
        return False, ping


