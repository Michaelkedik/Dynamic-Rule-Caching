#!/usr/bin/python


import signal
import sys
import os
import json
import time
import csv

from ptf.packet import IP
from scapy.sendrecv import sniff, sendp
from scapy.layers.inet import UDP
from scapy.all import *

host = sys.argv[1]
hostIP = sys.argv[2]
cacheSize = int(sys.argv[3])
rules = []
hits = {}
miss = {}
flows = {}
random.seed(5)
start = time.time()


def handle_pkt(pkt):
    global rules
    global host
    global hits
    global miss
    global start

    prob = random.random()

    if (pkt[IPv6].payload.load == 'done'):
        end = time.time()
        with open(host+'_'+str(cacheSize)+'.csv', 'w') as csvfile:
            fieldnames = ['flows_dst', 'flows_num', 'hits_dst', 'hits_num', 'miss_dst', 'miss_num', 'rules']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Find the maximum number of rows needed
            max_rows = max(len(flows), len(hits), len(miss), len(rules))

            # Iterate through the range of maximum rows
            for i in range(max_rows):
                row = {}

                # Flow column
                if i < len(flows):
                    flow_key = list(flows.keys())[i]
                    flow_value = list(flows.values())[i]
                    row['flows_dst'] = flow_key
                    row['flows_num'] = flow_value
                else:
                    row['flows_dst'] = ''
                    row['flows_num'] = ''

                # Hit column
                if i < len(hits):
                    hit_key = list(hits.keys())[i]
                    hit_value = list(hits.values())[i]
                    row['hits_dst'] = hit_key
                    row['hits_num'] = hit_value
                else:
                    row['hits_dst'] = ''
                    row['hits_num'] = ''

                # Miss column
                if i < len(miss):
                    miss_key = list(miss.keys())[i]
                    miss_value = list(miss.values())[i]
                    row['miss_dst'] = miss_key
                    row['miss_num'] = miss_value
                else:
                    row['miss_dst'] = ''
                    row['miss_num'] = ''

                # Rules column
                if i < len(rules):
                    row['rules'] = rules[i]
                else:
                    row['rules'] = ''

                writer.writerow(row)

        pkt = IPv6(dst='2001:1:5::1') / UDP(sport=80, dport=400) / 'done'
        send(pkt)
        pkt = IPv6(dst='2001:1:6::1') / UDP(sport=80, dport=400) / 'done'
        send(pkt)
        print("TIME IS -- "+str(end-start))
        return

    rule_dst = (pkt[IPv6].payload.load, pkt[UDP].dport)
    print(rule_dst)

    if rule_dst in flows:
        flows[rule_dst] += 1
    else:
        flows[rule_dst] = 1

    if rule_dst in rules:
        rule_index = rules.index(rule_dst)
        for i in range(rule_index + 1, len(rules)):
            rules[i - 1] = rules[i]
        rules[len(rules) - 1] = rule_dst

        if rule_dst in hits:
            hits[rule_dst] += 1
        else:
            hits[rule_dst] = 1
        pkt = IPv6(dst=rule_dst[0]) / UDP(sport=pkt[UDP].sport, dport=rule_dst[1])
    else:
        if rule_dst in miss:
            miss[rule_dst] += 1
        else:
            miss[rule_dst] = 1
        if prob < 0.5:
            pkt = IPv6(dst='2001:1:5::1') / UDP(sport=pkt[UDP].sport, dport=rule_dst[1]) / rule_dst[0]
        else:
            pkt = IPv6(dst='2001:1:6::1') / UDP(sport=pkt[UDP].sport, dport=rule_dst[1]) / rule_dst[0]

    if (rule_dst not in rules):
        if (len(rules) < cacheSize):
            rules.append(rule_dst)
        else:
            # minimum = min(flows , key = flows.get)
            # if flows[rule_dst] > flows[minimum] and minimum in rules :
            # rules.remove(minimum)
            # rules.append(rule_dst)
            for i in range(1, len(rules)):
                print(rules[i - 1], rules[i])
                rules[i - 1] = rules[i]
            rules[len(rules) - 1] = rule_dst

    send(pkt)


print("Will print a line for each UDP packet received...")

sniff(count=0, store=False, filter="udp and src host not " + hostIP, prn=lambda x: handle_pkt(x))

