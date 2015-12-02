#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#          - Artur Baruchi <abaruchi AT ncc DOT unesp DOT br>
#
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod
import subprocess
import os
import re


class NicInterface (object):
    '''
    This class returns all information regarding a NIC Interface.
    '''

    def __init__(self, nic_name):
        self._nic_name = nic_name
        self._nic_numa_node = self.nic_numa_node
        self._is_mellanox = self.is_mellanox_nic

    @property
    def nic_name(self):
        return self._nic_name

    @property
    def nic_numa_node(self):
        infile = ''
        numa_file = "/sys/class/net/" + self.nic_name + "/device/numa_node"
        try:
            infile = open(numa_file, 'r')
            numa_nic_node = infile.readline().rstrip()
        except IOError as erro:
            print "Erro: %s" % erro
        finally:
            infile.close()
        return numa_nic_node

    @property
    def is_mellanox_nic(self):
        nic_name = self.nic_name
        mellanox_nic = False
        for line in os.popen("ethtool -i " + nic_name):
            if 'mlx' in line:
                mellanox_nic = True

        return mellanox_nic


class NumaNodes(object):
    '''
    This class returns all CPUs in a given Numa
    '''
    def __init__(self, numa_node):
        self._numa_node = numa_node
        self._cpus_in_numa = self.cpus_in_numa

    @property
    def numa_node(self):
        return self._numa_node

    @property
    def cpus_in_numa(self):
        all_cpus = []
        nic_numa_node = self.numa_node
        node_line = "node " + str(nic_numa_node) + " cpus:"
        cmd = subprocess.Popen('numactl --hardware', shell=True,
                                   stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if node_line in line:
                cpus_regex = re.compile('(\d+)+')
                all_cpus = cpus_regex.findall(line)

        # Remove first one. It is the numa_node itself
        return all_cpus[1:]


class IRQBalancing(object):
    __metaclass__ = ABCMeta
    '''
    Class to Balance IRQ among CPUs in NUMA Nodes
    '''
    def __init__(self, nics_to_balance):
        self.nics_to_balance = nics_to_balance

    @abstractmethod
    def balance_irq(self):
        pass


class BalanceOneNic(IRQBalancing):

    def balance_irq(self):

        nic = NicInterface(self.nics_to_balance)
        if nic.is_mellanox_nic:
            numa_node = NumaNodes(nic.nic_numa_node)
            my_cpus = ",".join(numa_node.cpus_in_numa)
            print "Balancing One Nic"
            subprocess.call(['set_irq_affinity_cpulist.sh',
                            my_cpus, nic.nic_name])


class BalanceMoreNics(IRQBalancing):

    def balance_irq(self):

        interfaces_same_numa = {}
        interfaces_data = []
        first_cpu = 0
        last_cpu = 0

        for interface in self.nics_to_balance:
            temp_interface = NicInterface(interface)
            interfaces_data.append(temp_interface)

        for i in range(0,len(interfaces_data)-1):
            if (interfaces_data[i].is_mellanox_nic and
                    interfaces_data[i+1].is_mellanox_nic):
                if (interfaces_data[i].nic_numa_node ==
                        interfaces_data[i+1].nic_numa_node):
                    if (interfaces_data[i].nic_numa_node not in
                            interfaces_same_numa):
                        interfaces_same_numa[interfaces_data[i].\
                            nic_numa_node] = []

                        interfaces_same_numa[interfaces_data[i].\
                            nic_numa_node].\
                            append(interfaces_data[i].nic_name)

                        interfaces_same_numa[interfaces_data[i].\
                            nic_numa_node].\
                            append(interfaces_data[i+1].nic_name)
                    else:
                        interfaces_same_numa[interfaces_data[i].\
                            nic_numa_node].\
                            append(interfaces_data[i].nic_name)

                        interfaces_same_numa[interfaces_data[i].\
                            nic_numa_node].\
                            append(interfaces_data[i+1].nic_name)

        for key in interfaces_same_numa:
            div = len(interfaces_same_numa[key])
            my_numa = NumaNodes(key)
            last_cpu = len(my_numa.cpus_in_numa)/div
            for nic in interfaces_same_numa[key]:
                my_cpus = ",".join(my_numa.cpus_in_numa[first_cpu:last_cpu])
                print ("Balancing IRQ ...")
                subprocess.call(['set_irq_affinity_cpulist.sh',
                                my_cpus, nic])
                first_cpu = last_cpu
                last_cpu *= 2


def CommandArgs():

    parser = ArgumentParser()
    parser.add_argument("-e", "--ether", dest="nics",
                            help="Ethernet list for NUMA balancing.", type=str)
    args = parser.parse_args()
    nics_list = args.nics.split(',')
    return nics_list


if __name__ == '__main__':
    my_nics = CommandArgs()
    print my_nics

    number_of_nics = len(my_nics)
    if number_of_nics is 1:
        nic = BalanceOneNic(my_nics[0])
        nic.balance_irq()
    else:
        nic = BalanceMoreNics(my_nics)
        nic.balance_irq()

