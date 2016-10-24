# Ansible Scripts

Scripts inside this folder aims to automate tunning configurations for SC 
machines. For more information about Ansible, check 
[here](http://www.ansible.com/).

Please, note that, this procedure should be run inside the **host** 
(physical machine) and not inside the Virtual Machine.

# Usage

In order to create the environment to run SDN Demo, please, run the
following commands:

1. Execute the script `sdndemo_prep.sh` script as follow as root:
    
    ```
    # ./sdndemo_prep.sh centos
    ```
    
    or, if you are using Ubuntu:
    
    ```
    # ./sdndemo_prep.sh ubuntu
    ```
    
    This script will prepare the environment to execute the Ansible 
    playbook. It will install necessary tools and the Open vSwitch.

2. Now, you can run the playbook as follow:

    ```
    # ansible-playbook -v demosdn_playbook.yml
    ```

3. If everything goes fine, you should be able to start the virtual 
machines VM01 and VM02.

    ```
    # virsh start vm01
    # virsh start vm02
    ```
    
    Try to ping virtual machines:
    
    ```
    # ping -c 3 vm01
    # ping -c 3 vm02
    ```

4. Now, inside the virtual machines, you should force the usage of
SDN network. Basically, VM01 will be using VM02 as router. 

    First, clone this repository in both virtual machines.
    
    Command to run inside VM01:
    ```
    # cd DataTransfer/SDN_DEMO/scripts
    # ./start_sdn client on
    ```
    
    Command to run inside VM02:
    ```
    # cd DataTransfer/SDN_DEMO/scripts
    # ./start_sdn router on
    ```

## Cleanup 

You can remove all the configuration as follow:

1. Roll back the VM configuration:

    Command to run inside VM01:
    ```
    # cd DataTransfer/SDN_DEMO/scripts
    # ./start_sdn client off
    ```
    
    Command to run inside VM02:
    ```
    # cd DataTransfer/SDN_DEMO/scripts
    # ./start_sdn router off
    ```

2. Shutdown the VM:
    ```
    # virsh shutdown vm01
    # virsh shutdown vm02
    ```

3. Remove the topology and all Open vSwitches instances:
    
    ```
    # cd DataTransfer/Ansible/SDN_DEMO/scripts/
    # ./topo_create.sh wipe
    ```

With this procedure you will stop all VMs and all Open vSwitch 
instances. However, your VMs and Network configuration in libvirt will 
remain (not undefined).
