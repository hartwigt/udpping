#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################
## UDP Listener Server
##################################################
## GNU Affero General Public License v3.0
##################################################
## Author: Hartwig Tronnier
## Co-Author: Eric Sobian
## Version: 1.1.0
## Maintainer: Hartwig Tronnier
## Email: hartwig-git@online.de
## Status: BETA
##################################################
##
## Purpose of this program:
## receives a stream of sequentially numbered udp packets on given port (see 'udpsend.py')
## and reports any missing/duplicate/out-of-sequence packets
##
## We use this in network environments to measure convergence times in case of redundancy failovers
##
## Typically, each test client sends to every other client and listens for every other client
##
###################################################

import asyncio
import struct
import getopt
import sys, time, datetime, platform,signal
from datetime import datetime

mof = sys.stdout
class GracefulKiller:
  living = True
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum,frame):
    self.living=False

class EchoServerProtocol:
    
    def connection_made(self, transport):
        self.transport = transport
        self.expect = 1
        self.check = 1
        self.timeout = 0

    def datagram_received(self, data, addr):
        message = struct.unpack('>L', data)[0]
        missed = message - self.expect
        if (missed or plot) :
          mof.write(' '.join((str(datetime.now())[:-3],str(missed),' missed packets before ',str(message),'\n')))

        self.expect = message + 1
        self.timeout = 0

    def check_timeout(self):
        if self.check == self.expect :
           # self.expect will change on every received packet
           # check_timeout is called once a second, but it may only print if no packet was received in the meantime
           #
           # only print timeout message if it's the first one for this period or if plot mode is on
           if ((self.timeout == 0) or (plot == 1)) :
              mof.write(' '.join((str(datetime.now())[:-3],str(self.expect),' timeout \n')))
              self.timeout = 1
        else:
            self.check = self.expect
        
        
        
def main(argv): 
    global mof
    global plot
    outfile = ''
    port = 0
    plot = 1
    try:
        opts, args = getopt.getopt(argv, "hso:p:",["ofile=","port="])
    except getopt.GetoptError:
        print (__name__," [-h] [-s] -o outfile -p port")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('UDP listener:\n')
            print ('expects numbered packets to <port>, prints misses\n')
            print ("udplisten [-g] -o outfile -p port")
            print ("with -s (silent mode) will not write repeated timeouts or \"0 missed packets\" for every received packet, making output short for human evaluation\n")
            sys.exit(2)
        elif opt in ("-o","--ofile"):
          outfile = arg
        elif opt in ("-p","--port"):
          port = arg
        elif opt == '-s':
          plot = 0

    if port==0:
        print ("No port given!\n udplisten [-h] [-s] -o outfile -p port")
        sys.exit(2)
        
    if outfile == "":
        mof=sys.stdout
    else:
        mof=open(outfile,'a')
    loop = asyncio.get_event_loop()
    print("Starting UDP server, logging to ", outfile)
    mof.write(' '.join(('started at',str(datetime.now())[:-3],'on port',str(port),'on host',platform.node(),'\n')))
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=('::0', port))
    print("created endpoint:")
    transport, protocol = loop.run_until_complete(listen)

    killer = GracefulKiller()
    while killer.living:
        protocol.check_timeout()
        loop.run_until_complete(asyncio.sleep(1))
    print("Stopping...")
    mof.write(' '.join(('stopped at',str(datetime.now())[:-3],'on port',str(port),'on host',platform.node(),'\n')))

    transport.close()
    loop.close()
    mof.close()
        
if __name__ == "__main__":
  main(sys.argv[1:])        
