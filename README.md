# 1 .TCP Server-Client implementation in C

If we are creating a connection between client and server using TCP then it has few functionality like, TCP is suited for applications that require high reliability, and transmission time is relatively less critical. It is used by other protocols like HTTP, HTTPs, FTP, SMTP, Telnet. TCP rearranges data packets in the order specified. There is absolute guarantee that the data transferred remains intact and arrives in the same order in which it was sent. TCP does Flow Control and requires three packets to set up a socket connection, before any user data can be sent. TCP handles reliability and congestion control. It also does error checking and error recovery. Erroneous packets are retransmitted from the source to the destination.

## Preview :
<p align="center" >
  <img src="https://i.imgur.com/sCYWv50.png"  alt="accessibility text">
</p>

### The entire process can be broken down into following steps:

#### TCP Server – 

1) using create(), Create TCP socket.
2) using bind(), Bind the socket to server address.
3) using listen(), put the server socket in a passive mode, where it waits for the client to approach the server to make a connection
4) using accept(), At this point, connection is established between client and server, and they are ready to transfer data.
5) Go back to Step 3.

#### TCP Client – 

1) Create TCP socket.
2) connect newly created client socket to server.

## Compilation – 

### Server side: 
> gcc server.c -o server 
> <br>
> ./server

### Client side: 
> gcc client.c -o client 
> <br>
> ./client

# 2. Handling multiple clients on server with multithreading using Socket Programming in C
In the previous basic model **(section 1)**, the server handles only one client at a time, which is a big assumption if one wants to develop any scalable server model.
The simple way to handle multiple clients would be to spawn a new thread for every new client connected to the server. 

## Semaphores: 
Semaphore is simply a variable that is non-negative and shared between threads. This variable is used to solve the critical section problem and to achieve process synchronization in the multiprocessing environment.

#### sem_post: 
sem_post() increments (unlocks) the semaphore pointed to by sem. If the semaphore’s value consequently becomes greater than zero, then another process or thread blocked in a sem_wait(3) call will be woken up and proceed to lock the semaphore.

```bash
#include <semaphore.h>
int sem_post(sem_t *sem);
```
#### sem_wait: 
sem_wait() decrements (locks) the semaphore pointed to by sem. If the semaphore’s value is greater than zero, then the decrement proceeds and the function returns, immediately. If the semaphore currently has the value zero, then the call blocks until either it becomes possible to perform the decrement (i.e., the semaphore value rises above zero), or a signal handler interrupts the call.

```bash
#include <semaphore.h>
int sem_wait(sem_t *sem);
```
### Implementation :
For the server-side, create two different threads; a reader thread, and a writer thread. First, declare a serverSocket, an integer, a variable to hold the return of socket function.

```bash
int serverSocket = socket(domain, type, protocol);
```

- **serverSocket**: Socket descriptor, an integer (like a file-handle).
- **domain**: Integer, communication domain e.g., AF_INET (IPv4 protocol), AF_INET6 (IPv6 protocol).
- **type**: Communication type.
- **SOCK_STREAM**: TCP(reliable, connection-oriented).
- **SOCK_DGRAM**: UDP(unreliable, connectionless).
- **protocol**: Protocol value for Internet Protocol(IP), which is 0. This is the same number that appears on the protocol field in the IP header of a packet.(man protocols for more details).

Then, after initializing all the necessary variables bind the socket.

#### bind: 
After the creation of the socket, the bind function binds the socket to the address and port number specified in addr(custom data structure). In the example code, we bind the server to the local host, hence INADDR_ANY is used to specify the IP address.

```bash
int bind(int sockfd, const struct sockaddr *addr, 
         socklen_t addrlen);
```
#### listen: 
It puts the server socket in a passive mode, where it waits for the client to approach the server to make a connection. The backlog defines the maximum length to which the queue of pending connections for sockfd may grow. If a connection request arrives when the queue is full, the client may receive an error with an indication of ECONNREFUSED.

```bash
int listen(int sockfd, int backlog);
```
### Approach  –

1) After accepting the connection to the desired port, receive an integer from the client that defines the choice for reading or writing. Choice 1 indicates reader, while choice 2 indicates writer.
2) After successfully receiving data, call for pthread_create to create reader threads and writer threads.
3) After making successful connections to the server-client asks the user for input on the choice variable.
4) After getting the choice from the user, the client then sends this choice to the server to call the reader or writer thread by creating a client thread for the request.
## Compilation – 

### Server side: 
> gcc server.c -o server -pthread
> <br>
> ./server

### Client side: 
> gcc client.c -o client -pthread
> <br>
> ./client

