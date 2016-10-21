# Ansible Scripts

Scripts inside this folder aims to automate tunning configurations for SC 
machines. For more information about Ansible, check [here](http://www.ansible.com/).

# Usage

In order to run all playbook run:
```
$ ansible-playbook sc15_playbook.yml
```

By default ansible playbook will create ifcfg or interface configuration file

* For CentOS or Red Hat based server:
Files created are /etc/sysconfig/network-scripts/ifcfg-ethX and 
/etc/sysconfig/network-scripts/ifcfg-ethY. 

* For Ubuntu or Debian based server:
File created is /etc/network/interfaces.ansible

If the interface name and IP is known you can run the ansible playbook as
following:
```
$ ansible-playbook "-e 'VAR1=value1 VAR2=value2'" sc15_playbook.yml
```
Possible Variables are:
* IF_NAME_01 or IF_NAME_02: Interface name;
* IF_VLAN_01 or IF_VLAN_02: Vlan ID used;
* IF_IP_01 or IF_IP_02: IP address;
* IF_MASK_01 or IF_MASK_02: Network mask;
* IF_GW_01 or IF_GW_02: Default gateway for that interface;
* IF_MTU_01 or IF_MTU_02: MTU size (in bytes) used for that interface;
* BASE_DIR: By default, it must be run from root home directory. Change the base dir if 
it is not the case.

**Example 01**

Interface name is en0 with IP 192.168.10.23, netmask 255.255.254.0 and VLAN 200. 
This command will create the file /etc/sysconfig/network-scripts/ifcfg-en0.ansible or 
/etc/network/interfaces.ansible with the configuration parameters.
```sh
$ ansible-playbook sc15_playbook.yml -e "IF_NAME_01=en0 IF_IP_01=192.168.10.23 IF_MASK_01=255.255.254.0 IF_VLAN_01=200" 

```

**Example 02**

We also can configure two interfaces, eth2 and eth5 as follow:
```sh
$ ansible-playbook sc15_playbook.yml -e "IF_NAME_01=eth2 IF_IP_01=192.168.10.23 IF_MASK_01=255.255.254.0 IF_VLAN_01=200 IF_NAME_02=eth5 IF_IP_02=10.0.0.10 IF_VLAN_02=10"
```

## Prerequisites

Before running the Ansible scripts please make sure that following 
prerequisites are satisfied.

* SSH Keys are exchanged between nodes;
* User used by Ansible MUST have root access;
* Ansible package should be installed. 
For details refer [here](http://docs.ansible.com/ansible/intro_installation.html);
* Edit ansible/hosts file (in local directory) with the proper IP addresses.
* For git clone and git push using HTTPS, run the following command:
```
$ cd /root/
$ export GIT_SSL_NO_VERIFY=true
$ git clone https://git.ncc.unesp.br/sdn/sc15.git
```
Please, observe that base directory is /root/sc15/ansible/. If you clone it in other directory
than root home, run ansible as follow:
```
$ ansible-playbook sc15_playbook.yml  -e BASE_DIR=$PWD
```
* The proper device driver for the NICs used during the Demo MUST be installed. 
It creates ifcfg or interface configuration files with the proper parameters.
