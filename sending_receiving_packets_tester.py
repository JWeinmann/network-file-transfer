import Packet
import socket
import os
import time

sending_pkt = Packet.Packet()
receiving_pkt = Packet.Packet()

def build_pkt():
    os.system('clear')
    print('Build a packet\n')
    seq = int(input("seq: "))
    ack = int(input("ack: "))
    len = int(input("len: "))
    fin = int(input("fin flag: "))
    ackFlag = int(input("ack flag: "))
    syn = int(input("syn flag: "))
    rst = int(input("rst flag: "))
    # data = int(input("data: "))
    sending_pkt.setSegment("SEQ",seq)
    sending_pkt.setSegment("ACK",ack)
    sending_pkt.setSegment("LEN",len)
    sending_pkt.setFlag("ACK", bool(ackFlag))
    sending_pkt.setFlag("SYN", bool(syn))
    sending_pkt.setFlag("FIN", bool(fin))
    sending_pkt.setFlag("RST", bool(rst))
    os.system('')


print('is this the client or the server?')
type = input()
os.system('clear')

if type == 'client':
    print("This is the client. What port is the server listening on?")
    port = int(input("Port: "))
    os.system('clear')
    print("This is the client. The server is on port ",port)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    addr = ('localhost', port)
else:
    print("This is the server. What port should the server listen on?")
    port = int(input("Port: "))
    os.system('clear')
    print("This is the server listening on ",port,".")
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('localhost',port))

if type == 'client':
    build_pkt()
    input("press enter when ready to send first packet to server")
    sock.sendto(sending_pkt.packet(), addr)
    data, server = sock.recvfrom(10) # gets "it is the same" or "  not the same"
    print("Response: ",data)
    print("From: ",server)
else:
    build_pkt()
    print("waiting for packet")
    data, address = sock.recvfrom(45)
    receiving_pkt.copyPacket(data)
    print("Received packet: ", receiving_pkt.packet())
    if sending_pkt.packet() == receiving_pkt.packet():
        sock.sendto(b'it is the same',address)
    else:
        sock.sendto(b'  not the same',address)

'''




# These are the 4 tests you can choose from
choices = ["0 - Test sending (to the tester) one correctly constructed packet","1 - Test receiving (from the tester) one packet with specific segment/flag values","2 - Test sending 10 packets of length 45 (tester will list the 10 packets it received afterward)","3 - Test receiving 10 packets of length 45 (tester will list the 10 packets it sent afterward)"]
print("\nOf the following, what do you want to test? (Input the number)\n")
for c in choices:
    print(c)
test = input("\nYour choice: ")

if test == "0":
    print("\nSend the packet and I\'ll tell you what I got.")
'''



'''
# ***********************************************************************************
# Choose whether you are the client or server then configure the tester appropriately
print("Are you the client or server? (type \'client\' or \'server\'): ")
type = input()
while True:
    if type == 'client': # tester is the server
        sock.bind(server_address)
        os.system('clear')
        print("\nTester is the server and is on localhost and port 5002")
        break
    if type == 'server': # tester is the client
        os.system('clear')
        print("\nTester is the client and assumes you\'re on localhost and port 5002")
        sock.bind(server_address)
        break
    os.system('clear')
    print("Selection has to be \'client\' or \'server\': ")
    type = input()
# ***********************************************************************************
print("Tester is on 127.0.0.1 port 5002 and assumes you're connecting from 127.0.0.1")
'''
