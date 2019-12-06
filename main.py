import Packet
import socket
import Director
import FileInteract
import time
from concurrent.futures import ThreadPoolExecutor

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = ('localhost', 10001)
client_address = ('localhost',10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.setblocking(0)

director = Director.Director()

def listen():
    inData, address = sock.recvfrom(45)
    if inData:
        print("Received packet")
    outData = director.incoming(inData)
    if outData: # in hand-shake
        sent = sock.sendto(outData,address)

def talk():
    try:
        #print("trying to send")
        outData = director.trySend()
    except Exception as e:
        pass
    if outData:
        sent = sock.sendto(outData,client_address)



with ThreadPoolExecutor() as executor:
    while True:
        time.sleep(0.1)
        f1 = executor.submit(listen)
        f2 = executor.submit(talk)
