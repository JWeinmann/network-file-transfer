import Packet
import socket
import Director
import FileInteract
from concurrent.futures import ThreadPoolExecutor

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_address = ('localhost', 10001)
client_address = ('localhost',10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.setblocking(0)

director = Director.Director()

lock = False


def listen():




    data, address = sock.recvfrom(45)
    while not lock:
        pass
    lock = True
    if data:
        print("\nlister received the following:  ",data)
    director.incoming(data)
    lock = False


def talk():
#    print("talking")


    while not lock:
        pass
    lock = True

    input("hit enter to send \'hello\' to client")
    sent = sock.sendto(b'hello',client_address)
    if not director.established or director.connecting:
        return False
    if not director.canSend():
        return False
    lock = False


with ThreadPoolExecutor() as executor:
    while True:
        f1 = executor.submit(listen)
        f2 = executor.submit(talk)
