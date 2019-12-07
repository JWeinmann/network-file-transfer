import Packet
import socket
import Director
import FileInteract
import time
import threading
from concurrent.futures import ThreadPoolExecutor

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = ('localhost', 12222)
client_address = False
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
#sock.setblocking(0)

director = Director.Director()
scrapPacket = Packet.Packet()

lock = threading.Lock()

def listen():

    inData = None
    inData, address = sock.recvfrom(1500)
    lock.acquire()
    global client_address
    if not client_address:
        client_address = address
    try:
        outData = director.incoming(inData)
    finally:
        lock.release()
    if inData:
        print("********** Received Packet From Client **********\n",director.inPacket.summary())

    if outData: # in hand-shake
        sent = sock.sendto(outData,client_address)

def talk():
    outData = None
    #time.sleep(0.01)
    try:
        #print("trying to send")
        lock.acquire()
        try:
            outData = director.trySend()
        finally:
            lock.release()
    except Exception as e:
        print("Exception: ",e)
    if outData:
        sent = sock.sendto(outData,client_address)
        scrapPacket.shallowCopy(outData)
        print("********** Sending Packet To Client **********\n",scrapPacket.summary())


while True:

    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=talk)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


'''
with ThreadPoolExecutor() as executor:
    while True:
        #time.sleep(0.1)
        f1 = executor.submit(listen)
        f2 = executor.submit(talk)
'''
