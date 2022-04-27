# 1 .TCP Server-Client implementation in Python

If we are creating a connection between client and server using TCP then it has few functionality like, TCP is suited for applications that require high reliability, and transmission time is relatively less critical. It is used by other protocols like HTTP, HTTPs, FTP, SMTP, Telnet. TCP rearranges data packets in the order specified. There is absolute guarantee that the data transferred remains intact and arrives in the same order in which it was sent. TCP does Flow Control and requires three packets to set up a socket connection, before any user data can be sent. TCP handles reliability and congestion control. It also does error checking and error recovery. Erroneous packets are retransmitted from the source to the destination.

## Preview :
<p align="center" >
  <img src="https://i.imgur.com/sCYWv50.png"  alt="accessibility text">
</p>

# 2 . Socket Programming with Multi-threading in Python

## Prerequisite : [Socket Programming in Python](https://www.geeksforgeeks.org/socket-programming-python/) , [Multi-threading in Python](https://www.geeksforgeeks.org/multithreading-python-set-1/)
<pre>from _thread import *
import threading</pre>
### Socket Programming : 
It helps us to connect a client to a server. Client is message sender and receiver and server is just a listener that works on data sent by client.
### What is a Thread ?  
A thread is a light-weight process that does not require much memory overhead, they are cheaper than processes.
### What is Multi-threading Socket Programming ? 
Multithreading is a process of executing multiple threads simultaneously in a single process.
### Multi-threading Modules : 
A _thread module & threading module is used for multi-threading in python, these modules help in synchronization and provide a lock to a thread in use. 


## Compilation – 

### Server side: 
> python server.py


### Client side: 
> python client.py


