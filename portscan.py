import argparse
from queue import Queue

from modules.Router import Router
from modules.TreminalParser import TerminalParser


def main():
    arguments = TerminalParser()
    args = arguments.extract_terminal_params()
    targets = concat_targets(args.targets)
    router = Router(args.addr,
                    args.timeout,
                    args.max_threads,
                    args.verbose,
                    args.guess,
                    targets)
    router.start()


def concat_targets(targets):
    result = []

    for target in targets:
        tmp_single = target['single']
        tmp_multiple = target['multiple']
        for single_port in tmp_single:
            result.append(single_port)
        for multiple_ports in tmp_multiple:
            start, end = int(multiple_ports[1]), int(multiple_ports[2]) + 1

            for port in range(start, end):
                result.append((multiple_ports[0], port))
    return result


if __name__ == '__main__':
    main()
