# Docker helper methods

from __future__ import print_function

import socket
import sys

__author__ = 'sknop'


def docker_real_name():
    hostname = socket.gethostname()

    with open('/etc/hosts') as f:
        content = f.read()

    lines = content.splitlines()
    host_entries = [ x.split('\t') for x in lines ]

    ip = None

    for e in host_entries:
        k,v = e
        if v == hostname:
            ip = k

    if ip:
        candidates = [ x[1] for x in host_entries
                        if x[0] == ip and x[1] != hostname and not x[1].endswith(".bridge")]

        # should be exactly one candidates:
        if len(candidates) > 1:
            print("More than one hostname candidate found: {}".format(candidates))
            print("Bugging out for safety reasons")
            sys.exit(1)

        # if there is none we are down the deep end anyway
        if len(candidates) == 0:
            print("No candidate found in /etc/hosts: {}".format(host_entries))
            print("Bugging out for safety reasons")
            sys.exit(1)

        return candidates[0]
    else:
        print("We have not found our IP address from hostname {} and this /etc/hosts {}".format(hostname, host_entries))
        print("Bugging out")
        sys.exit(1)
