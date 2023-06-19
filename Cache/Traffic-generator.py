#!/usr/bin/python

from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send
from scapy.all import *
import sys
import random
import threading
import time



def send_pkts(IP_list,large_list,small_ports,UE_ADDR,seed,threads):
    random.seed(seed)
    for i in range(150/threads):
        prob = random.random()
        # type A flows
        if prob < 0.5:
            PAYLOAD = random.choice(IP_list)
            dst_port = random.choice(large_list)
            for i in range(300):
                pkt = IPv6(dst=UE_ADDR) / UDP(sport=80, dport=dst_port) / PAYLOAD
                send(pkt, loop=False, verbose=True)
        #type B flows
        else:
            PAYLOAD = random.choice(IP_list)
            dst_port = random.choice(small_ports)
            for i in range(30):
                pkt = IPv6(dst=UE_ADDR) / UDP(sport=80, dport=dst_port) / PAYLOAD
                send(pkt, loop=False, verbose=True)
    pkt = IPv6(dst=UE_ADDR) / UDP(sport=80, dport=dst_port) / 'done'
    send(pkt, loop=False, verbose=True)




UE_ADDR = ['2001:1:1::a','2001:1:2::a','2001:1:3::a','2001:1:4::a']

IP_h1 = ['2001:1:2::1','2001:1:3::1','2001:1:4::1']
IP_h2 = ['2001:1:1::1','2001:1:3::1','2001:1:4::1']
IP_h3 = ['2001:1:1::1','2001:1:2::1','2001:1:4::1']
IP_h4 = ['2001:1:1::1','2001:1:2::1','2001:1:3::1']
large_ports = [i for i in range (22000,23001)]
small_ports = [i for i in range (22000,22026)]


host = sys.argv[1]
threads = int(sys.argv[2])
if host == 'h1':
    for i in range(threads):
        threading.Thread(target=send_pkts, args=(IP_h1,large_ports,small_ports,UE_ADDR[0],5,threads)).start()
        time.sleep(0.1)
elif host == 'h2':
    for i in range(threads):
        threading.Thread(target=send_pkts, args=(IP_h2,large_ports,small_ports,UE_ADDR[1],10,threads)).start()
        time.sleep(0.1)
elif host == 'h3':
    for i in range(threads):
        threading.Thread(target=send_pkts, args=(IP_h3,large_ports,small_ports,UE_ADDR[2],15,threads)).start()
        time.sleep(0.1)
elif host == 'h4':
    for i in range(threads):
        threading.Thread(target=send_pkts, args=(IP_h4,large_ports,small_ports,UE_ADDR[3],20,threads)).start()
        time.sleep(0.1)
else:
    pass

