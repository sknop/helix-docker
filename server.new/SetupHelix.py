#! /usr/bin/env python2.7

from __future__ import print_function

import argparse
import os
import sys
import subprocess
import P4

__author__ = 'sknop'

CONFIGURATION = [ 'dm.user.noautocreate=1',
                  'security=3' ]

# if server.existing does not exist
#  create server.existing (Case?, Unicode?)
#  verify user and password work as super user
# else
#  check case sensitivity
#  create user/password
#  configure basic security on server.existing
#
# Start Server
#
# --case-sensitive (default), --case-insensitive
# --unicode, --no-unicode (default)
# --user USER
# --password PASSWORD
# [ --use-protocol TCP|SSL|TCP6 etc ]

def check_server(root, log, case, unicode):
    db_rev = os.path.join(root, "db.rev")
    if os.path.exists(db_rev):
        # we have a server.existing already, nothing to do here
        return None

    case_option = ""
    if case:
        case_option = "-C{}".format(case)

    if unicode:
        cmd = "p4d -r {root} {case} -xi".format(root=root, case=case_option)
        subprocess.call(cmd, shell=True)

    rsh_port = "rsh:p4d -r {root} -i -L {log} {case}".format(root=root, log=log, case=case_option)
    p4 = P4.P4(port=rsh_port)
    with p4.connect():
        p4.run_info()

    return rsh_port

def setup_helix(port, user, password, unicode):
    p4 = P4.P4()
    p4.port = port
    p4.user = user

    if unicode:
        p4.charset='auto'

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

def start_helix(root, port, log):
    """Starts p4d by replacing this script with the p4d image.
     Never returns"""

    cmd = "p4d -r {root} -p {port} -L {log}".format(root=root, port=port, log=log).split()
    os.execvp("p4d", cmd) # and this is the last thing this process will ever see

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Helix Setup")
    parser.add_argument("-u", "--user", help="P4USER", required=True)
    parser.add_argument("-P", "--password", help="P4PASSWD", required=True)
    parser.add_argument("-C", "--case", type=int, choices=[0,1], help="Case sensitivity, ignored if Server exists")
    parser.add_argument("-U", "--unicode", action='store_true', help="Set Server to Unicode, ignore if server.existing exists")

    options = parser.parse_args()

    port = "1666"
    user = options.user
    password = options.password
    case = options.case
    unicode = options.unicode

    if "P4ROOT" in os.environ:
        root = os.environ["P4ROOT"]
    else:
        print("No P4ROOT defined, bailing out")
        sys.exit(1)

    if "P4LOG" in os.environ:
        log = os.environ["P4LOG"]
    else:
        print("No P4LOG defined, bailing out")
        sys.exit(2)

    rsh_port = check_server(root, log, case, unicode)
    if rsh_port:
        setup_helix(rsh_port, user, password, unicode)
    else:
        print("Server already exists, please use image sknop/perforce-server-existing")
        sys.exit(3)

    start_helix(root, port, log)