#! /usr/bin/env python2.7

from __future__ import print_function

import argparse
import P4
import uuid
import os
import errno
import sys

__author__ = 'sknop'


class SetupSwarm:
    def __init__(self, port, user, password, swarmuser, swarmpass):
        self.swarmuser = swarmuser
        self.swarmpass = swarmpass

        self.p4 = P4.P4()

        self.create_token()
        self.setup_helix(port, user, password)

    def create_token(self):
        """Create the token"""

        path = "/opt/perforce/swarm/data/queue/tokens"

        # ensure the directory is there
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

        token_name = str(uuid.uuid1()).upper()
        filename = os.path.join(path, token_name)

        os.mknod(filename)

    def setup_helix(self, port, user, password):
        self.p4.port = port
        self.p4.user = user

        with self.p4.connect() as p4:
            p4.password = password
            p4.run_login()

            # verify current user is super user
            protects = p4.run_protects(tagged=False)
            found = False

            for p in protects:
                if p.startswith("super user {}".format(p4.user)):
                    found = True

            if not found:
                print("User {} is not super user. Aborting".format(p4.user))
                sys.exit(1)

            # create swarm user - if it does not exist
            if len(p4.run_users(self.swarmuser,exception_level=1)) == 0:
                userspec = p4.fetch_user(self.swarmuser)
                userspec._fullname = "Swarm Administrator"
                p4.save_user(userspec, "-f")

            # update the password, previous password *will* be overwritten
            p4.run("passwd","-P",self.swarmpass, self.swarmuser)

            # create swarm group - if it does not exist, and add swarm to it
            groups = p4.run_groups(tagged=False)
            if self.swarmuser not in groups:
                groupspec = p4.fetch_group(self.swarmuser)
                groupspec._timeout = "unlimited"
                groupspec._users = [ self.swarmuser ]
                p4.save_group(groupspec)

            # add swarm as admin to the protection table, if not there already
            protects = p4.run_protects("-u", self.swarmuser, tagged=False)
            found = False

            for p in protects:
                if p.startswith("admin user {}".format(self.swarmuser)):
                    found = True

            if not found:
                protections = p4.fetch_protect()
                protections._protections.append("admin user {} * //...".format(self.swarmuser))
                p4.save_protect(protections)

            # submit the trigger files


            # and update the trigger table

    def need_protects(self, p4, permission, user=None):
        protects = None
        if user:
            protects = p4.run_protects("-u", user, tagged=False)
        else:
            protects = p4.run_protects(tagged=False)

        for p in protects:
            if p.startswith("{} user".format(permission)):
                return False

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Helix Setup")
    parser.add_argument("-p", "--port", help="P4PORT", required=True)
    parser.add_argument("-u", "--user", help="P4USER (super user)", required=True)
    parser.add_argument("-P", "--password", help="P4PASSWD", required=True)
    parser.add_argument("-s", "--swarmuser", help="Swarm User", default="swarm")
    parser.add_argument("-S", "--swarmpass", help="Swarm Password", default="Swarmpass")

    options = parser.parse_args()

    port = options.port
    user = options.user
    password = options.password
    swarmuser = options.swarmuser
    swarmpass = options.swarmpass

    swarm = SetupSwarm(port, user, password, swarmuser, swarmpass)
