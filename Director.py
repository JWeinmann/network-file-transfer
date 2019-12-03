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
        self.established = False # is True if a connection is established and data transmission should occur
        self.connecting = False # is True if a handshake is/should be occuring
        self.windowNum = 100 # number of windows - will change throughout connection
        self.windowDeque = deque(maxlen=self.windowNum) # a queue holding the packets in the window
        self.overflowDeque = deque(maxlen=self.windowNum) # ************* what's this again?
        self.timeDeque = deque(maxlen=self.windowNum)  # a queue holding the timeout times for each corresponding packet in the window

    ''' handle incoming packet '''
    ''' Returns:
          True if it's a valid and expected packet
          False if not (corrupted, or something else) '''
    def incoming(self, pkt: bytes):
        self.packet.copyPacket(pkt)
        ''' check if the packet has been corrupted '''
        if not self.packet.isgood():
            print("*** Received packet is corrupted -- ignoring ***")
            return False
        ''' check if the client is asking for the connection to abruptly abort '''
        if self.packet.getFlag("rst"):
            self.established = self.connecting = False
        ''' check if connection not established '''
        if not self.established or self.connecting:
            return self.openingShake()
        


    ''' this function is called if a packet is received when a connection is not currently established '''
    ''' it constructs the appropriate responding packet and returns True if something should be sent to the client '''
    ''' returns False if something is wrong with the packet and it should be ignored '''
    def openingShake(self):
        if not self.established: # if this passes, then the received packet should be the first handshake
            if self.packet.getSegment("seq") == 45 and self.packet.getSegment("ack") == 0 and self.packet.getFlag("SYN") and not self.packet.getFlag("ACK"):
                self.connecting = True
                self.established = True
                self.packet.setSegment("seq",90)
                self.packet.setSegment("ack",45)
                self.packet.setFlag("ack",True)
                return True
            else: return False # if else, then the 1st handshake is not done right so ignore
        # the following elif succeeds if a valid 3rd handshake is received, so transmission can begin
        elif self.packet.getSegment("seq") == 135 and self.packet.getSegment("ack") == 90 and not self.packet.getFlag("SYN") and self.packet.getFlag("ACK"):
            self.connecting = False # the connection has been established
            return True
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
d.established = 45
d.connecting = False
p2.shpacket()
print(d.incoming(p2.packet()))
