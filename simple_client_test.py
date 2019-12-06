import socket
import Packet
import sys
import time


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
myaddress = ('localhost', 10000)
address = ('localhost',10001)
print('starting up on {} port {}'.format(*myaddress))
sock.bind(myaddress)

packet = Packet.Packet()

i = 0
input("press entre to start")
while True:
    time.sleep(0.1)
    if i == 0: # simulate first hand-shake
        packet.setSegment("SEQ",45)
        packet.setSegment("LEN",45)
        packet.setFlag("SYN", True)
        sock.sendto(packet.packet(), address)
    if i == 1:
        packet.setSegment("SEQ",135)
        packet.setSegment("LEN",45)
        packet.setSegment("ACK",90)
        packet.setFlag("SYN", False)
        packet.setFlag("ACK",True)
        sock.sendto(packet.packet(), address)
    if i > 1:
        pass
    print('\nwaiting to receive')
    data, address = sock.recvfrom(4096)
    packet.shallowCopy(data)
    print('received {} bytes from {}'.format(
        len(data), address))
    print('received:  ',packet.summary())
    '''
    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(
            sent, address))
    '''

    i = i+1
