#!/usr/bin/python


import signal
import sys
import os

Cache = sys.argv[1]
threads = sys.argv[2]
repository_path_pc = ' ~/Desktop/Amit/ngsdn-tutorial/'
host  =['h1a','h2a','h3a','h4a','h5','h6']
command = ['sudo docker cp mininet:/root/',repository_path_pc]
for i in host:
    print(command[0]+i+'_'+Cache+'.csv'+command[1]+threads+'/'+Cache+'/'+i+'_'+Cache+'.csv')
    os.system(command[0]+i+'_'+Cache+'.csv'+command[1]+threads+'/'+Cache+'/'+i+'_'+Cache+'.csv')


