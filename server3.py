#samuel kyama muasya
#p15-42924/2017

# load the sockets and Struct module
import socket
import struct
import time

from gossip_functions import *

# create a reliable TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get  local hostname
local_hostname = socket.gethostname()

# get complete domain name for this computer
local_complete_domain_name = socket.getfqdn()

# the ip address associated with the fqdn
ip_address = socket.gethostbyname(local_hostname)

# display hostname, domain name and IP address
print ("Details are as follows %s (%s) with %s" % (local_hostname, local_complete_domain_name, ip_address))

# bind the socket to the port 12345
server_address = (ip_address, 12347)
print ('Starting the server on %s port %s' % server_address)
sock.bind(server_address)
updated_at = []
updated_at.append(time.time())
# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)
multiplication_result = 1
while True:
    # wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print ('connection from', client_address)

        # get the data in bits
        while True:
            data = connection.recv(64)
            #ask for the last updated time and compare with that of the device requesting gossip
            if data.decode('utf-8') == 'q':
                # encode last updated time as
                #get the second last element
                if len(updated_at) >1:
                    last_time_updated = struct.pack("f", updated_at[-2])
                elif len(updated_at) == 0:
                    last_time_updated = struct.pack("B", -1)
                else:
                    last_time_updated = struct.pack("f", updated_at[0])
                connection.send(last_time_updated)
            else:
                if data:
                    #now that data has been received, set the epidemic status
                    epidemic_status = 'infected'
                    # Multiply values
                    message_to_gossip=data.decode('utf-8')

                    print ("message is: %s" % message_to_gossip)
                    updated_at.append(time.time())

                else:
                    #all the data has been received
                    break
                #get data and convert it to bytes
                message_as_bytes =  message_to_gossip.encode('utf-8')
                current_message=message_as_bytes
                #send the data to the client
                connection.send(message_as_bytes)



    #let's make sure this code is excecuted even in the case of an exception
    finally:
        print("start connecting to another node")



