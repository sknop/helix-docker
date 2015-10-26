#! /usr/bin/env python2.7

from __future__ import print_function

import argparse
import P4
import uuid
import os
import errno
import sys
import shutil

import DockerHelper

__author__ = 'sknop'


class SetupSwarm:
    def __init__(self, port, user, password, swarmuser, swarmpass):
        self.swarmuser = swarmuser
        self.swarmpass = swarmpass
        self.token = str(uuid.uuid1()).upper()
        self.swarm_host = DockerHelper.docker_real_name()

        self.p4 = P4.P4()

        self.create_token()
        self.setup_helix(port, user, password)

    def create_token(self):
        """Create the token"""

        path = "/opt/perforce/swarm/data/queue/tokens"

        # ensure the directory is there
        mkdir_p(path)

        filename = os.path.join(path, self.token)
        os.mknod(filename)

    def setup_helix(self, port, user, password):
        self.p4.port = port
        self.p4.user = user

        with self.p4.connect() as p4:
            p4.password = password
            p4.run_login()

            # verify current user is super user
            if self.need_protects(p4, "super"):
                print("User {} is not super user. Aborting".format(p4.user))
                sys.exit(1)

            self.ensure_swarm_user(p4)
            self.create_triggers(p4)

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

    def ensure_swarm_user(self, p4):
        # create swarm user - if it does not exist
        if len(p4.run_users(self.swarmuser,exception_level=1)) == 0:
            userspec = p4.fetch_user(self.swarmuser)
            userspec._fullname = "Swarm Administrator"
            p4.save_user(userspec, "-f")

        # update the password, previous password *will* be overwritten
        p4.input = [ self.swarmpass, self.swarmpass ]
        p4.run("passwd", self.swarmuser)

        # create swarm group - if it does not exist, and add swarm to it
        groups = p4.run_groups(tagged=False)
        if self.swarmuser not in groups:
            groupspec = p4.fetch_group(self.swarmuser)
            groupspec._timeout = "unlimited"
            groupspec._users = [ self.swarmuser ]
            p4.save_group(groupspec)

        # add swarm as admin to the protection table, if not there already
        if self.need_protects(p4, "admin", user=self.swarmuser):
            protections = p4.fetch_protect()
            protections._protections.append("admin user {} * //...".format(self.swarmuser))
            p4.save_protect(protections)

    def create_triggers(self, p4):
        # ensure .swarm depot exists
        depotspec = p4.fetch_depot('.swarm')
        p4.save_depot(depotspec)

        # create a temporary client
        client_name = "tmp_swarm_setup"
        clientspec = p4.fetch_client(client_name)
        clientspec._root = '/tmp/' + client_name
        clientspec._host = ""

        mkdir_p(clientspec._root)

        clientspec._view = ["//.swarm/triggers/... //{}/...".format(client_name)]
        p4.save_client(clientspec)

        p4.cwd = clientspec._root
        p4.client = client_name

        # copy the files into the correct location
        trigger_file = "/opt/perforce/swarm-triggers/bin/swarm-trigger.pl"
        if os.path.isfile(trigger_file):
            # copy the file
            shutil.copy(trigger_file, clientspec._root)

        else:
            print("Swarm-triggers not installed successfully, bugging out")
            sys.exit(1)

        config_file = os.path.join(clientspec._root, "swarm-trigger.conf")

        with open(config_file, 'w') as f:
            print('SWARM_HOST="http://{}"'.format(self.swarm_host), file=f)
            print('SWARM_TOKEN={}'.format(self.token), file=f)
            print('ADMIN_USER=', file=f)
            print('ADMIN_TICKET_FILE=', file=f)

        p4.run_add('swarm-trigger.pl')
        p4.run_add('swarm-trigger.conf')
        p4.run_submit('-d', 'Swarm trigger and configuration added')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

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
