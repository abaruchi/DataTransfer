#!/bin/bash

## Description:
## This script is used to install and configure pre-reqs to run sdn demo
##
## Usage: install_prereq.sh [centos | ubuntu | check]
##
## Options:
##   centos - Install pre-req in CentOS
##	 ubuntu - Install pre-req in Ubuntu
##   check  - Verify if this script run before 
##
## Authors:
##          - Artur Baruchi <abaruchi AT ncc DOT unesp DOT br>

#### Constants
CHECK_FILE="/var/tmp/.pre_req"

#### Functions

check () 
{
	if [ -e $CHECK_FILE ]
	then
		echo 1
	else
		echo 0
	fi
}

set_as_check ()
{
	date -u > $CHECK_FILE
}

centos ()
{
	DIR_RPMBUILD="$HOME/rpmbuild"

	echo "---- Installing Pre-Reqs for a CENTOS ----"
	echo
	echo
	echo "-- Installing packages --"
	yum -y install epel
	
	yum -y install make gcc openssl-devel autoconf automake rpm-build redhat-rpm-config \
	python-devel openssl-devel kernel-devel kernel-debug-devel libtool wget
	
	yum -y install ansible
	
	echo "-- Installing Open vSwitch --"
	mkdir -p $DIR_RPMBUILD/SOURCES/ ; cd $DIR_RPMBUILD/SOURCES/
	wget http://openvswitch.org/releases/openvswitch-2.5.1.tar.gz
	tar xzvf openvswitch-2.5.1.tar.gz
	
	sed 's/openvswitch-kmod, //g' openvswitch-2.5.1/rhel/openvswitch.spec > openvswitch-2.5.1/rhel/openvswitch_no_kmod.spec
	rpmbuild -bb --nocheck openvswitch-2.5.1/rhel/openvswitch_no_kmod.spec
	yum localinstall $DIR_RPMBUILD/RPMS/x86_64/openvswitch-2.5.1-1.x86_64.rpm
	systemctl start openvswitch.service
	chkconfig openvswitch on
	
	# Create the check file
	set_as_check
}

ubuntu ()
{
	echo "---- Installing Pre-Reqs for a UBUNTU ----"
	echo
	echo
	echo "-- Installing packages --"
	
	apt-get --yes --force-yes install ansible gcc openssl-devel autoconf automake \
	python-devel openssl-devel kernel-devel kernel-debug-devel libtool wget
	
	apt-get --yes --force-yes install openvswitch-datapath-source \
	openvswitch-datapath-source openvswitch-common openvswitch-switch

	# Create the check file
	set_as_check
}

#### Main

case $1 in
check)
	code=check
	exit $code
	;;
centos)
	centos
	exit 0
	;;
ubuntu)
	ubuntu
	exit 0
	;;
*)
	echo "ERROR: Invalid Args."
	;;
esac