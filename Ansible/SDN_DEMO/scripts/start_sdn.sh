#!/bin/bash

## This script is used to enable and disable the VM usage of SDN
## Usage:
##   start_sdn.sh [client | router] [on | off]
## Authors:
##          - Artur Baruchi <abaruchi AT ncc DOT unesp DOT br>


#### Constants
export INT_IFACE=eth0 # Internal network, connected to Open vSwitch
export EXT_IFACE=eth1 # External network, connected to Internet

#### Functions

enable_client ()
{
	case $1 in
	on)
           if [ -e /var/tmp/.last_timestamp ]; then
              echo
              echo "-- This host is already running as client --"
              echo "-- If this is wrong, please run:          --"
              echo "-- ./start_sdn.sh client off              --"
            exit 0
           fi

	   CONTINUE=N
	   echo "WARNING: You may lost connection."
	   echo -n "Do you wish to Continue? [y/N]:  "
	   read CONTINUE

	   if [ $CONTINUE == "n" ] || [ $CONTINUE == "N" ]; then
	       echo "Exiting..."
	       exit 0
	   elif [ $CONTINUE == "y" ] || [ $CONTINUE == "Y" ]; then
	       timestamp=`date +%H%M%S%d%m%y`
               echo $timestamp > /var/tmp/.last_timestamp
               ifdown eth1
               route add default gw 10.10.1.5
               cp -p /etc/resolv.conf /etc/resolv.conf.$timestamp
               > /etc/resolv.conf
               echo "nameserver 8.8.8.8" >> /etc/resolv.conf
               echo "nameserver 8.8.4.4" >> /etc/resolv.conf
           else
               echo "Exiting..."
               exit 0
           fi
       ;;
       off)
        rm -rf /var/tmp/.last_timestamp
        ifup eth1
       ;;
       *)
        echo "Wrong Arg - Use start or stop"
       ;;
       esac
}

enable_router ()
{
    INT_IFACE=eth0 # Internal network, connected to Open vSwitch
    EXT_IFACE=eth1 # External network, connected to Internet

    case $1 in
	on)
          sysctl -w net.ipv4.ip_forward=1
          /sbin/iptables -t nat -A POSTROUTING -o $EXT_IFACE -j MASQUERADE

          /sbin/iptables -A FORWARD -i $EXT_IFACE -o $INT_IFACE -m state \
          --state RELATED,ESTABLISHED -j ACCEPT

          /sbin/iptables -A FORWARD -i $INT_IFACE -o $EXT_IFACE -j ACCEPT
        ;;
        off)
          sysctl -w net.ipv4.ip_forward=0
          /sbin/iptables -t nat -D POSTROUTING -o $EXT_IFACE -j MASQUERADE

          /sbin/iptables -D FORWARD -i $EXT_IFACE -o $INT_IFACE -m state \
          --state RELATED,ESTABLISHED -j ACCEPT

          /sbin/iptables -D FORWARD -i $INT_IFACE -o $EXT_IFACE -j ACCEPT
        ;;
        *)
          echo "Wrong Arg - Use start or stop"
          ;;
    esac
}

help ()
{
        echo
        echo "Usage: "
        echo "start_sdn.sh [client | router ] [on | off ]"
        echo "client: Configure VM as client"
        echo "server: Configure VM as router"
        echo
}


#### Main

case $1 in
    client)
        if [ $2 == "on" ]; then
           enable_client on
        elif [ $2 == "off" ]; then
           enable_client off
        else
           help
        fi
        ;;
    router)
        if [ $2 == "on" ]; then
           enable_router on
        elif [ $2 == "off" ]; then
           enable_router off
        else
           help
        fi
        ;;
    *)
        help
     ;;
     esac
