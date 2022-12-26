#!/bin/bash
DIR=$(dirname $(readlink -f $0))
cd $DIR

screen -S python-ip-logger -dm bash -i -c ./run-forever.sh
