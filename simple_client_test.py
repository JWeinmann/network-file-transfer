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

image = bytearray()

input("press enter when ready to send first packet")
# first packet to inituate handshake
packet.setSegment("SEQ",45)
packet.setSegment("LEN",45)
packet.setFlag("SYN", True)
print('sending: ',packet.summary())
sock.sendto(packet.packet(), address)

jump = False

def listen():
    inData, address = sock.recvfrom(4096)
    if inData:
        inpacket.shallowCopy(inData)
        print('received:  ',inpacket.summary())
        image.append(inpacket.packet()[45:])
        if inpacket.getFlag("FIN"):
            jump = True

def respond():

    packet.setSegment("ACK",inpacket.getSegment("SEQ"))
    packet.setSegment("LEN",45)
    packet.setSegment("SEQ",packet.getSegment("ACK")+45)
    packet.setFlag("SYN", False)
    packet.setFlag("ACK",True)
    print('sending: ',packet.summary())
    sock.sendto(packet.packet(), address)


with ThreadPoolExecutor() as executor:
    while True:
        time.sleep(0.1)
        f1 = executor.submit(listen)
        f2 = executor.submit(respond)
        print(image)
        if jump:
            break

f = open('received_image.jpg','wb')
f.write(image)
f.close()
