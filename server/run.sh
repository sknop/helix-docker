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

check_environment

P4USER=${P4USER:-p4admin}
P4PASSWD=${P4PASSWD:-Password}

if [ -f $P4ROOT/db.rev ]; then
    echo "$P4ROOT/db.rev already exists, bugging out of here"
else 
    python2.7 /SetupHelix.py -p "rsh:/opt/perforce/sbin/p4d -r ${P4ROOT} -i -L ${P4LOG}" -u ${P4USER} -P ${P4PASSWD}
fi

# start server

p4d -r $P4ROOT -L $P4LOG -p $P4PORT
