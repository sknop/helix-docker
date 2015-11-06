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

if [ ! -f $P4ROOT/db.rev ]; then
    echo "Server does not exist. Please specify volume with existing server files"
    echo "or use sknop/perforce-server-new image."
    exit 1
fi

# start server.existing

p4d -r $P4ROOT -L $P4LOG -p $P4PORT
