import Packet
from collections import deque
from functools import *

''' need to figure out if this is a good strategy:
incoming packet:
- corrupt? -> ignore
- ACK one lower than expected? -> retart window
- lower ACK that? -> ignore
    - assumes it's a duplicate
- higher ACK? -> move window up to that point

- problems with that:
    - lots of duplicates will restart the window many times
'''


class Director:

    def __init__(self) -> None:
        self.packet = Packet.Packet()
        self.client = None
        self.connected = False
        self.windowNum = 100
        self.windowDeque = deque(maxlen=self.windowNum)
        self.timeDeque = deque(maxlen=self.windowNum)

    ''' handle incoming packet '''
    def incoming(self, packet: bytes):
        self.packet.copyPacket(packet)
        ''' check if corrupted '''
        if not self.packet.isgood():
            return
        ''' check if connection not established '''
        if not self.client or not self.connected:
            self.openingShake()
            return

    ''' called if packets from unknown client are received '''
    def openingShake(self):
        pass


    def restartWindow(self) -> None:
        self.windowDeque.clear()
        self.timeDeque.clear()




p = Packet.Packet()
p.setFlag("SYN",True)
p.shpacket()

#sequence = p.getSegment("SEQ")
sequence = partial(p.getSegment,"SEQ")
print(sequence())
p.setSegment("SEQ", 5)
print(sequence())
a = sequence
print(a)

d = Director()
d.incoming(p.packet())
#print(d.packet.packet())
#print(d.packet.packet())
d.restartWindow()



'''
print(d.windowDeque)
print(d.windowNum)
print(d.timeDeque)
'''
