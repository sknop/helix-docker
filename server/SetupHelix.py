#! /usr/bin/env python2.7

from __future__ import print_function

import argparse
import P4

__author__ = 'sknop'

CONFIGURATION = [ 'dm.user.noautocreate=1',
                  'security=3' ]

def setup_helix(port, user, password):
    p4 = P4.P4()
    p4.port = port
    p4.user = user

    with p4.connect():
        # create user
        myuser = p4.fetch_user()
        p4.save_user(myuser, '-f')

        # set password
        p4.run_password('', password)

        # login with new password
        p4.password = password
        p4.run_login()

        # update configuration
        for c in CONFIGURATION:
            p4.run_configure('set', c)

        # set default protection table
        protect = p4.fetch_protect()
        p4.save_protect(protect)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Helix Setup")
    parser.add_argument("-p", "--port", help="P4PORT", required=True)
    parser.add_argument("-u", "--user", help="P4USER", required=True)
    parser.add_argument("-P", "--password", help="P4PASSWD", required=True)

    options = parser.parse_args()

    port = options.port
    user = options.user
    password = options.password

    setup_helix(port, user, password)
