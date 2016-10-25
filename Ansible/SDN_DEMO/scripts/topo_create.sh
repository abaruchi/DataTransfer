#!/bin/bash

## Description:
## This script is used to create a topology to be used as testbed to SDN demo.
##
## Usage: topo_create.sh [no_loop | loop | wipe]
##
## Options:
##   no_loop topology looks like:
##
##   vm01 -- s1 -- s2 -- vm02
##
##	 loop topology looks like:
##
##	    	 |--- s2 --- |
##   vm01 -- sw1-             -s3 -- vm02
##		 |--- s4 --- |
##
## Authors:
##          - Artur Baruchi <abaruchi AT ncc DOT unesp DOT br>

#### Constants
CONTROLLER="127.0.0.1"
PORT="6633"
LINK_BANDWIDTH=2000000
MTU=9000

#### Functions

common ()
{
    ovs-vsctl set interface vm01 ingress_policing_burst=$LINK_BANDWIDTH
    ovs-vsctl set interface vm01 ingress_policing_rate=$LINK_BANDWIDTH
    ovs-vsctl set interface vm02 ingress_policing_rate=$LINK_BANDWIDTH
    ovs-vsctl set interface vm02 ingress_policing_burst=$LINK_BANDWIDTH

    for bridge in s1 s2 s3 s4; do
        for port in `ovs-vsctl list-ports $bridge`; do
            ip link set mtu $MTU dev $port 2> /dev/null
        done
    done
}

loop ()
{
	echo "-- Creating a loop topology --"
	echo "---- Creating Virtual Switches ----"
	for i in s1 s2 s3 s4; do
		ovs-vsctl add-br $i
		sleep 2
	done

	echo "---- Linking Switch Ports ----"

	ovs-vsctl -- add-port s1 patch14 \
	-- set interface patch14 type=patch options:peer=patch41 \
	-- add-port s4 patch41 \
	-- set interface patch41 type=patch options:peer=patch14


	ovs-vsctl -- add-port s1 patch12 \
	-- set interface patch12 type=patch options:peer=patch21 \
	-- add-port s2 patch21 \
	-- set interface patch21 type=patch options:peer=patch12

	ovs-vsctl -- add-port s4 patch43 \
	-- set interface patch43 type=patch options:peer=patch34 \
	-- add-port s3 patch34 \
	-- set interface patch34 type=patch options:peer=patch43

	ovs-vsctl -- add-port s2 patch23 \
	-- set interface patch23 type=patch options:peer=patch32 \
	-- add-port s3 patch32 \
	-- set interface patch32 type=patch options:peer=patch23

	echo "---- Setting  Controller ----"
	for i in s1 s2 s3 s4; do
		ovs-vsctl set-controller $i tcp:$CONTROLLER:$PORT
		sleep 2
	done

    common
	echo "---- Topology Setup Done ----"
	ovs-vsctl show
}

no_loop ()
{
	echo "-- Creating a loop free topology --"
	echo "---- Creating Virtual Switches ----"
	for i in s1 s2 s3; do
		ovs-vsctl add-br $i
		sleep 2
	done

	echo "---- Linking Switch Ports ----"

	ovs-vsctl -- add-port s1 patch12 \
	-- set interface patch12 type=patch options:peer=patch21 \
	-- add-port s2 patch21 \
	-- set interface patch21 type=patch options:peer=patch12

	ovs-vsctl -- add-port s2 patch23 \
	-- set interface patch23 type=patch options:peer=patch32 \
	-- add-port s3 patch32 \
	-- set interface patch32 type=patch options:peer=patch23

	echo "---- Setting  Controller ----"
	for i in s1 s2 s3; do
		ovs-vsctl set-controller $i tcp:$CONTROLLER:$PORT
		sleep 2
	done
    common

	echo "---- Topology Setup Done ----"
	ovs-vsctl show
}

wipe ()
{
	NUM_BRIDGES=`ovs-vsctl list-br | wc -l`

	case $NUM_BRIDGES in
	3)
		PORTS="patch12 patch21 patch23 patch32"
		BRIDGES="s1 s2 s3"
		;;
	4)
		PORTS="patch14 patch41 patch12 patch21 patch43 patch34 patch23 patch32"
		BRIDGES="s1 s2 s3 s4"
		;;
	0)
		echo "-- No Configuration Found --"
		echo
		exit 0
		;;
	*)
		echo "-- Cannot Run in this System --"
		echo
		exit 1
		;;
	esac

	echo "---- Removing Ports ----"
	echo "---- $PORTS ----"
	for port in $PORTS; do
		ovs-vsctl del-port $port
		sleep 2
	done
	echo

	echo "---- Removing Bridges ----"
	echo "---- $BRIDGES ----"
	for br in $BRIDGES; do
		ovs-vsctl del-br $br
		sleep 2
	done
	echo
}

help ()
{
	echo "Usage: "
	echo "topo_create.sh [no_loop | loop | wipe]"
	echo
	echo "no_loop: Topology is loop free"
	echo "loop: Topology has a loop"
	echo "wipe: Destroy any topology created by this script"
	echo
	exit 0
}

#### Main

case $1 in
loop)
	loop
	exit 0
	;;
no_loop)
	no_loop
	exit 0
	;;
wipe)
	wipe
	exit 0
	;;
*)
	help
	;;
esac