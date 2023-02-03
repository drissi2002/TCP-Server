# 1 .TCP Server-Client implementation in Python

If we are creating a connection between client and server using TCP then it has few functionality like, TCP is suited for applications that require high reliability, and transmission time is relatively less critical. It is used by other protocols like HTTP, HTTPs, FTP, SMTP, Telnet. TCP rearranges data packets in the order specified. There is absolute guarantee that the data transferred remains intact and arrives in the same order in which it was sent. TCP does Flow Control and requires three packets to set up a socket connection, before any user data can be sent. TCP handles reliability and congestion control. It also does error checking and error recovery. Erroneous packets are retransmitted from the source to the destination.

## Simulation:
<p align="center" >
  <img src="https://i.imgur.com/x7pXND4.png"  alt="accessibility text">
</p>

# 2 . Socket Programming with Multi-threading in Python

## Prerequisite : Socket Programming in Python, Multi-threading in Python

### Socket Programming : 
It helps us to connect a client to a server. Client is message sender and receiver and server is just a listener that works on data sent by client.
### What is a Thread ?  
A thread is a light-weight process that does not require much memory overhead, they are cheaper than processes.
### What is Multi-threading Socket Programming ? 
Multithreading is a process of executing multiple threads simultaneously in a single process.
### Multi-threading Modules : 
A _thread module & threading module is used for multi-threading in python, these modules help in synchronization and provide a lock to a thread in use. 

<pre>from _thread import *
import threading</pre>

A lock object is created by

<pre>from _thread import *
import threading</pre>

A lock has two states,**“locked”** or **“unlocked”**. It has two basic methods **acquire()** and **release()**. When the state is unlocked **print_lock.acquire()** is used to change state to locked and **print_lock.release()** is used to change state to unlock.
The function **thread.start_new_thread()** is used to start a new thread and return its identifier. The first argument is the function to call and its second argument is a tuple containing the positional list of arguments.
Let’s study client-server multithreading socket programming by code- 
Note:-The code works with python3. 
**Multi-threaded Server Code**

## Compilation – 

### Server side: 
> python server.py


### Client side: 
> python client.py

## Simulation:
#### Machine 1 : *Pc Portable* | Machine 2 : *Smartphone Android*
<p align="center" >
  <img src="https://i.imgur.com/AVvkH0O.jpg"  alt="accessibility text">
</p>

### Reference 
- [thread — Multiple threads of control](https://docs.python.org/2/library/thread.html)
- [Socket Programming in Python](https://www.geeksforgeeks.org/socket-programming-python/) 
- [Multi-threading in Python](https://www.geeksforgeeks.org/multithreading-python-set-1/)

### Copyrights 
<i>Spetial thanks to the team : <b >Drissi houcem eddine - Bouraoui manel - Tayari eya </b> </i>
<br>
<i>Spetial thanks to our mate **BEN MANSOUR Mehdi** for helping us in this Project</i>  💃



