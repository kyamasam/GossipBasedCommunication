import socket
import struct
import time

def init_gossip(port, updated_at, message_to_gossip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # local hostname
    local_hostname = socket.gethostname()
    updated_at = time.time()
    # full host name
    local_fqdn = socket.getfqdn()

    # get the according IP address
    ip_address = socket.gethostbyname(local_hostname)

    # bind the socket to the port 12345, and connect
    server_address = (ip_address, port)
    sock.connect(server_address)

    print("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
    # ask for the last updated time

    # convert int to Byte before sending to server
    query_time_updated = 'q'.encode('utf-8')

    # send message as bytes
    sock.sendall(query_time_updated)

    # listen for data from the server
    time_from_server = sock.recv(64)
    # receive the result from the server and convert it to int from byte
    server_updated_at = struct.unpack('f', time_from_server)

    # if this device has the latest update, then push that update
    # we use server_updated_at[0] in order to access the tupple as float
    if server_updated_at[0] < updated_at or server_updated_at == updated_at:
        # display result to terminal
        print(" we have the latest update \n")


        # convert int to Byte before sending to server
        message_as_bytes = message_to_gossip.encode('utf-8')

        # send message as bytes
        sock.sendall(message_as_bytes)

        # listen for data from the server
        data_from_server = sock.recv(64)
        # receive the result from the server and convert it to int from byte
        result_from_server = data_from_server.decode('utf-8')

        # display result to terminal
        print(" The gossiped message was : %s" % result_from_server)

    else:
        # server has a more recent update
        print("the server contains a more recent update, : %s ", server_updated_at)
        print("client updated at , : %s ", updated_at)

