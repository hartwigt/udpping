#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################
## UDP Sender
##################################################
## GNU Affero General Public License v3.0
##################################################
## Author: Hartwig Tronnier
## Co-Author: Eric Sobian
## Version: 1.1.1
## Maintainer: Hartwig Tronnier
## Email: hartwig-git@online.de
## Status: BETA
##################################################
##
## Purpose of this program:
## send a constant stream of sequentially numbered udp packets to a destination ip/port
## on the receiver side the partner program 'udplisten' watches for these packets 
## and reports any missing/duplicate/out-of-sequence packets
##
## We use this in network environments to measure convergence times in case of redundancy failovers
##
## Typically, each test client sends to every other client and listens for every other client
##
###################################################

import asyncio, sys, getopt
import socket
import struct
from threading import Timer
from time import sleep

## The asyncio construct is used to send timed packets without blocking the cpu
## since my use case involved starting many instances on each computer
## I used 10 instances on Raspberry Pi 3, Eric had 110 instances on virtual x86 machines

        
@asyncio.coroutine
def ping(mysock):
    cnt=1
    while True:
        yield from asyncio.sleep(.009)
        message = struct.pack('>L',cnt)
        mysock.sendto(message,(UDP_IP,UDP_PORT))
        cnt += 1
    
    
    
UDP_IP = "::1"
UDP_PORT = 0
UDP_PROTO=socket.AF_INET6

usage = "udpsend -a IP(v6)-address -p port -v Version(4 or 6)"

                    

    

try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:p:v:",["help","address=","port=","version="])
except getopt.GetoptError:
    print (usage)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h','--help'):
        print ('UDP sender:\n')
        print ('sends numbered packets to <address>:<port>\n')
        print (usage)
        sys.exit(2)
    elif opt in ("-a","--address"):
      UDP_IP = arg
    elif opt in ("-p","--port"):
      UDP_PORT = int(arg)
    elif opt in ("-v","--version"):
      if int(arg)==4:
        UDP_PROTO=socket.AF_INET

if UDP_PORT==0:
    print ("No port given!\n udplisten -o outfile -p port")
    sys.exit(2)

    
print("UDP send to ",UDP_IP,":",UDP_PORT," press ^C to abort\n")    
sock = socket.socket(UDP_PROTO, socket.SOCK_DGRAM) # UDP

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(ping(sock))
    loop.run_forever()
except KeyboardInterrupt:
    print("Stopping ...")
finally:
    loop.close()
    sleep(1)
    sock.close()

