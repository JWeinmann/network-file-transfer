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
        self.overflowDeque = deque(maxlen=self.windowNum)
        self.timeDeque = deque(maxlen=self.windowNum)
        #self.pkt = self.packet.packet()

    ''' handle incoming packet '''
    ''' Returns:
          True if it's a valid and expected packet
          False if not (corrupted, or something else) '''
    def incoming(self, pkt: bytes):
        self.packet.copyPacket(pkt)
        '''******** add code check for abort flag *********'''
        if not self.packet.isgood():
            print("*** Received packet is corrupted -- ignoring ***")
            return False
        ''' check if connection not established '''
        if not self.client or self.connecting or self.terminating:
            if self.terminating:
                print('****need to do this part****')
            return self.openingShake()

    def openingShake(self):
        if not self.client:
            if self.packet.getSegment("seq") == 45 and self.packet.getSegment("ack") == 0 and self.packet.getSegment("length") == 45:
                return True
            else: return False
        else:
            print('********3rd handshake**********')
        return "hey"



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

p2 = Packet.Packet()
p2.setSegment("seq",45)
p2.setSegment("length",45)
d.client = 45
d.connecting = False
p2.shpacket()
print(d.incoming(p2.packet()))
