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
        self.connecting = False
        self.terminating = False
        self.windowNum = 100
        self.windowDeque = deque(maxlen=self.windowNum)
        self.timeDeque = deque(maxlen=self.windowNum)
        #self.pkt = self.packet.packet()

    ''' handle incoming packet '''
    ''' Returns:
          True if it's a valid and expected packet
          False if not (corrupted, or something else) '''
    def incoming(self, pkt: bytes):
        self.packet.copyPacket(pkt)
        ''' check if corrupted '''
        if not self.packet.isgood():
            print("*** Received packet is corrupted -- ignoring ***")
            return False
        print("it is good")
        ''' check if connection not established '''
        if not self.client or not self.connected:
            return self.openingShake()


    ''' called if packets from unknown client are received '''
    def openingShake(self):
        pass



    def restartWindow(self) -> None:
        self.windowDeque.clear()
        self.timeDeque.clear()

d = Director()
print(d.windowDeque)
p = Packet.Packet()
p.setData(b'THIS IS DATA')
d.windowDeque.append(p.packet())
print(d.windowDeque)
d.windowDeque.append(233)
d.windowDeque.append(99999)
print(d.windowDeque)
win = d.windowDeque
win.popleft()
print(d.windowDeque)
