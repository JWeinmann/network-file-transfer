import socket
import Packet
import sys
import time

from concurrent.futures import ThreadPoolExecutor

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
myaddress = ('localhost', 10000)
address = ('localhost',10001)
print('starting up on {} port {}'.format(*myaddress))
sock.bind(myaddress)
sock.setblocking(0)

packet = Packet.Packet()
inpacket = Packet.Packet()

client_responses = [(180, 225), (4321, 4366), (8462, 8507), (12603, 12648), (16744, 16789), (20885, 20930), (25026, 25071), (29167, 29212), (33308, 33353), (37449, 37494), (41590, 41635), (45731, 45776), (49872, 49917), (54013, 54058), (58154, 58199), (62295, 62340), (66436, 66481), (70577, 70622), (74718, 74763), (78859, 78904), (83000, 83045), (87141, 87186), (91282, 91327), (95423, 95468), (99564, 99609), (103705, 103750), (107846, 107891), (111987, 112032), (116128, 116173)]

input("press enter when ready to send first packet")

packet.setSegment("SEQ",45)
packet.setSegment("LEN",45)
packet.setFlag("SYN", True)
print('sending: ',packet.summary())
sock.sendto(packet.packet(), address)


a=False

def listen():
    inData, address = sock.recvfrom(4096)
    if inData:
        inpacket.shallowCopy(inData)
        print('received:  ',inpacket.summary())
        a = True

def respond():

    packet.setSegment("ACK",inpacket.getSegment("SEQ"))
    packet.setSegment("LEN",45)
    packet.setSegment("SEQ",packet.getSegment("ACK")+45)
    packet.setFlag("SYN", False)
    packet.setFlag("ACK",True)
    print('sending: ',packet.summary())
    sock.sendto(packet.packet(), address)
    a=False

with ThreadPoolExecutor() as executor:
    while True:
        time.sleep(0.1)
        f1 = executor.submit(listen)
        f2 = executor.submit(respond)


'''
i = 0
input("press entre to start")
while True:
    if i == 0: # simulate first hand-shake
        packet.setSegment("SEQ",45)
        packet.setSegment("LEN",45)
        packet.setFlag("SYN", True)
        print('sending: ',packet.summary())
        sock.sendto(packet.packet(), address)
    if i == 1:
        packet.setSegment("SEQ",135)
        packet.setSegment("LEN",45)
        packet.setSegment("ACK",90)
        packet.setFlag("SYN", False)
        packet.setFlag("ACK",True)
        print('sending: ',packet.summary())
        sock.sendto(packet.packet(), address)
    if i > 1:
        packet.setSegment("ACK",inpacket.getSegment("SEQ"))
        packet.setSegment("SEQ",packet.getSegment("ACK")+45)
        print('sending: ',packet.summary())
        sock.sendto(packet.packet(), address)
    data, address = sock.recvfrom(4096)
    inpacket.shallowCopy(data)
    print('received:  ',inpacket.summary())
    '''
