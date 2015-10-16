#!/bin/bash
set -e

# P4PORT provided via environment
# P4ROOT provided via environment

function check_environment {
    if [ -z $P4PORT ]; then
        echo "P4PORT must be defined"
        exit 1
    fi

    if [ -z $P4ROOT ]; then
        echo "P4ROOT must be defined"
        exit 1
    fi

    if [ -z $P4LOG ]; then
        echo "P4LOG must be defined"
        exit 1
    fi
}

function create_config {
    mkdir -p /client
    cat >> /client/.p4 <<!
P4PORT=rsh:/opt/perforce/sbin/p4d -r $P4ROOT -i -L P4LOG
P4USER=$P4USER
P4CLIENT=setup.client
!
}

function setup_server {
    cd /client
    p4 user -f -o | p4 user -i
    p4 client -o  | p4 client -i

    echo Setting password to $P4PASSWD

    p4 passwd <<!
$P4PASSWD
$P4PASSWD
!

    p4 login <<!
$P4PASSWD
!

    # security settings
    p4 configure set dm.user.noautocreate=1
    p4 protect -o | p4 protect -i
    p4 configure set security=3
}

check_environment

P4USER=${P4USER:-p4admin}
P4PASSWD=${P4PASSWD:-Password}
export P4CONFIG=.p4

if [ -f $P4ROOT/db.rev ]; then
    echo "$P4ROOT/db.rev already exists, bugging out of here"
else 
    create_config
    setup_server
fi

# start server

p4d -r $P4ROOT -L $P4LOG -p $P4PORT
