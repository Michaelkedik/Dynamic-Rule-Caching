# Dynamic Rule Caching in Datacenter Networks

***Electrical and Computer Engineering, 4th Year Engineering Project.***

**Advisors:** Prof Chen Avin, Dr Gabriel Scalosub.

Switches in data center networks are tasked with storing a vast number of traffic rules, typically stored in an external device called a controller. However, accessing this controller slows down the network's performance. 
The project aims to address this issue by implementing Caching-based Acceleration Mechanisms, which utilize caching technologies and redistribute forwarding rules across different switches. This approach minimizes the need for frequent access to the controller, ultimately boosting the network's overall throughput.  
The project analysis demonstrates that dynamic rule caching in data centers substantially reduces the volume of packets routed to the controller, thus contributing to the expected network throughput enhancement.

## Technology
The project employed the following technology:  
**Mininet:** Network emulator that creates virtual hosts, switches, controllers, and links.  
**P4:** Domain-specific language for network devices, specifying packet processing in the data plane.  
**P4runtime:** Control plane specification for managing data plane elements of a P4-programmed device.  
**BMv2 Switch:** Software switch deployed on Mininet Switches, enabling control plane management through the data plane using P4Runtime.  
**ONOS:** Open-source SDN controller for next-gen SDN solutions.  

## The Method
To accomplish the project objectives, the initial step involved creating an emulation environment by integrating Mininet, ONOS, and P4-configured Bmv2 switches.The emulation environment featured a data center-like topology, which is depicted in the figure below.  

![image](https://github.com/Michaelkedik/Dynamic-Rule-Caching/assets/136968696/a1458b31-a1cb-4017-b175-aa12bb9a124d)


 Subsequently, a traffic generator was developed to simulate network traffic. Following that, Python and Scapy were utilized to implement the caching mechanisms. Two caching mechanisms, namely Fast Cache and Best Static, were implemented on each of the switches in the topology.

### Fast Cache
Upon packet arrival at a switch from a flow, the switch verifies if the flow's policy exists in the cache table. If the policy is found, it results in a hit. otherwise, it leads to a miss.  
**Hit**: The packet is directly forwarded to its destination without any intermediate steps.  
**Miss**: The flow's policy is inserted into the cache table if there is available space, otherwise, it replaces the least recently used policy.  
          The packet is then forwarded to the subsequent stage.

### Best Static:
The cache tables are statically populated with flow policies that achieved the highest hit ratio during a pre-run, prior to the experiment. The contents of the cache tables remain static and do not change. If the policy is found, it results in a hit. otherwise, it leads to a miss.  
**Hit**: The packet is directly forwarded to its destination without any intermediate steps.  
**Miss**: The packet is forwarded to the subsequent stage.  


## Environment Setup:
1. Open https://github.com/opennetworkinglab/ngsdn-tutorial and clone the repository using "git clone -b advanced https://github.com/opennetworkinglab/ngsdn-tutorial".  
2. Follow the installation guide on the Readme file, use "Option 2 - Manually install Docker and other dependencies".  
3. This tutorial contains several exercice, some of them are irrelavant to our project. Yet, in order to make sure that the setup of the enviroment will work we suggest coping all the files in the "solutions" repository to the corresponding place in the main repository "ngsdn-tutorial". In addition, we highly recommend following the steps in Exercises 3-6 in order to gain a deeper understanding of the process.  
4. Open "link to git" and clone the repository using "git clone -b advanced link to git".  
5. Replace the Makefile from the main repository "ngsdn-tutorial" with the Makefile from /Dynamic-Rule-Caching/Environment.  
6. add copyDocker form /Dynamic-Rule-Caching/Environment to the main repository "ngsdn-tutorial".  
7. Replace the netcfg.json and topo-v6.py files from the "ngsdn-tutorial/mininet" repository with those files from /Dynamic-Rule-Caching/Cache.    
Upon completing the aforementioned steps, an emulation environment will be established with the topology illustrated in the above figure. The switches utilized in the environment will be BMv2 switches, while the controller employed will be ONOS.
In order to modify the topology, changes need to be made to both the topo-v6.py and netcfg.json files. 

## Experiments
1. In the repository, `ngsdn-tutorial` open a terminal, run:  
   $ sudo make-start  
   $ sudo make-netcfg  
   $ sudo make-SRV6  
2. Open a terminal for each ToR host that receives packets and run:  
   $ sudo util/mn-cmd <host> mininet/recv-ToR <host> <host-ip> <cache size>  
    '''  
     host - The host that receives the packets. (in our topology : h1a,h2a,h3a,h4a)  
     host-ip - The IP address of the host above.  
     cache size - The size of the cache table.  
     example: sudo util/mn-cmd h1a mininet/recv-ToR h1a 2001:1:1::a 20  
    '''  
3. Open a terminal for each Aggregation host that receives packets and run:  
   $ sudo util/mn-cmd <host> mininet/recv-Agg <host> <host-ip> <cache size>  
    '''  
     host - The host that receives the packets. (in our topology : h5,h6)  
     host-ip - The IP address of the host above.  
     cache size - The size of the cache table.  
     example: sudo util/mn-cmd h5 mininet/recv-Agg h5 2001:1:5::1 20  
    '''  
4. Open a terminal for each host that generates traffic and run:  
   $ sudo util/mn-cmd <host> mininet/Traffic-generator <host> <threads>  
    '''  
     host - The host that generates the traffic. (in our topology : h1,h2,h3,h4)  
     threads - The number of threads that generate flows in parallel.  
     example: sudo util/mn-cmd h1 mininet/Traffic-generator h1 50  
    '''	  
5. Run: $ python copyDocker.py <ache size> <threads>  
    '''  
    cache size - The size of the cache table used in the experiment.  
    threads - The number of threads that generate flows in parallel in the experiment.  
    example: $ python copyDocker.py 20 50  
    Note: This script copies all the .csv files that were generated in the experiments from the docker to the computer.  
          To alter the destination of the copied files on the computer, make adjustments to the script by modifying the "repository_path_pc".
    '''    


## Origin work
1. Our project is based on:  
* ONOS - https://opennetworking.org/onos/  
* Mininet - http://mininet.org/  
* P4 - https://opennetworking.org/p4/  
* P4Runtime API - https://p4.org/p4-spec/p4runtime/main/P4Runtime-Spec.html  
* BmMv2 - https://github.com/p4lang/behavioral-model  
* ngsdn-tutorial - https://github.com/opennetworkinglab/ngsdn-tutorial  
2. Traffic protocol is based on scapy python package.  


## Useful links:  
1. *complete when ONOS wiki returns to work*  
