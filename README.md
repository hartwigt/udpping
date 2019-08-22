# udpping
UDP sender and listener for network convergence tests

In network projects we wanted to measure the impact of various defects on data transmission. For example, turning off a redundant router will disrupt traffic until the routing protocols detect the failure, and turning it on again can impact traffic during convergence.
We had the problem that no professional load generator was available and we had to find a way to do it with some virtual machines and some Raspberrys. 
Searching for a ping tool that could 
- write a protocol of packets received and lost
- with information on when the losses happen (one long pause or several short ones)
- with subsecond timing, ideally milliseconds
- ideally monitoring each direction separately

didn't yield anything usable. 

iperf was nearest, but did not provide information on when there was packet loss.
So we decided to write our own toolset.
Python libraries provided nearly everything needed - especially the asyncio lib has easy to use socket functions, which make sending and receiving datagrams quite easy.
Keeping to the *NIX-philosophy "one tool, one function" we created two programs, one to send udp packets to a given address/port, and one to listen for udp packets on a given port. The programs should be able to work with IPv4 and IPv6, and to accurately detect time and duration of losses and also out-of-order packets, the sender includes a counter-value in the payload.
The receiver is responsible for writing a protocol file.
Since typically many instances of both sender and listener will run on each test device (any-to-any tests), they should not consume much resources, especially not do busy waits. Also especially the listener needs a clean exit routine, so it is able to flush and close it's logfile when terminated. That's the reason for the asyncio loop construct.
USAGE:
Since all those redundancy failover tests typically disrupt management sessions, the programs are meant to get started, run on their own even if the shell terminates, and get killed by a script after the test. The script will collect the log files and evaluate them.
Eric (eric@sobian.de) wrote a nice gnuplot script to graphically display the timing.
For small setups with only a handful of connections the logfiles can be evaluated by hand.
udplisten has two modes:
In silent mode it will only write one line if timed out, and one line if there is a jump in received packet numbers. So you will have one pair of lines per interruption.
In plot mode (default) it will write one line per packet received, and one "timeout" line per second. This corresponds with the gnuplot script from Eric
When doing network convergence tests, of course each listener has to write a local logfile, since interactive sessions and network shares may break. Shell scripts (thanks Eric) are responsible for one-touch starting and stopping all instances and collecting the log files.


