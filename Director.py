import Packet
from collections import deque
from functools import *
import copy
import time
from timeit import default_timer as timer

from concurrent.futures import ThreadPoolExecutor

class Director:

    def __init__(self) -> None:
        self.outPacket = Packet.Packet() # used to build the outgoing packets
        self.inPacket = Packet.Packet() # used to read the incoming packets
        self.scrapPacket = Packet.Packet()
        self.terminating = False # True is final packet has been sent and just waiting for ACK
        self.established = False # is True if a connection is established and data transmission should occur
        self.connecting = False # is True if a handshake is/should be occuring
        self.windowNum = 100 # number of windows - will change throughout connection
        self.windowDeque = deque(maxlen=self.windowNum) # a queue holding the packets in the window
        #self.overflowDeque = deque(maxlen=self.windowNum) # ************* what's this again?
        self.timeDeque = deque(maxlen=self.windowNum)  # a queue holding the timeout times for each corresponding packet in the window
        self.timer = None # when the first packet in the window expires
        self.toi = 0.001 # time-out interval
        self.srtt = 0.0005 # sample round-trip time - last round-trip time
        self.ertt = 0.0005 # estimated / smoothed rount-trip time
        self.tsm = 0.0005 # time safety margin
        self.dataLocation = 0

    ''' handle incoming packet '''
    def incoming(self, pkt: bytes):
        self.inPacket.copyPacket(pkt)
        ''' check if the packet has been corrupted '''
        ''' *********** remove if client doesn't implement sha check
        if not self.inPacket.isgood():
            print("*** Received packet is corrupted -- ignoring ***")
            return False
        '''
        ''' check if the client is asking for the connection to abruptly abort '''
        if self.inPacket.getFlag("RST"):
            self.established = self.connecting = self.terminating = False
            return False
        ''' check if connection not established or is in starting handshake '''
        if not self.established or self.connecting:
            return self.openingShake()

        return self.processAck()

    ''' process the ack packet '''
    def processAck(self):
        self.scrapPacket.shallowCopy(self.windowDeque.popleft())
        if self.inPacket.getSegment("ACK") < self.scrapPacket.getSegment("SEQ"):
            self.windowDeque.appendleft(self.scrapPacket.packet())
            return
        elif self.inPacket.getSegment("ACK") == self.scrapPacket.getSegment("SEQ"):
            self.ackTime()
            self.timer = self.timeDeque.popleft()
            self.timeDeque.appendleft(self.timer)
            self.timer = self.timer + self.toi
            return
        while True:
            self.scrapPacket.shallowCopy(self.windowDeque.popleft())
            self.timeDeque.popleft()
            if self.inPacket.getSegment("ACK") == self.scrapPacket.getSegment("SEQ"):
                self.timeDeque.popleft()
                self.timer = self.timeDeque.popleft()
                self.timeDeque.appendleft(self.timer)
                self.timer = self.timer + self.toi
                break
        return



    ''' this function is called if a packet is received when a connection is not currently established '''
    ''' it constructs the appropriate responding packet and returns True if something should be sent to the client '''
    ''' returns False if something is wrong with the packet and it should be ignored '''
    def openingShake(self):
        if not self.established: # if this passes, then the received packet should be the first handshake, otherwise return false
            if self.inPacket.getSegment("SEQ") == 45 and self.inPacket.getSegment("ACK") == 0 and self.inPacket.getFlag("SYN") and not self.inPacket.getFlag("ACK"):
                self.connecting = True
                self.established = True
                self.outPacket.setSegment("SEQ",90)
                self.outPacket.setSegment("ACK",45)
                self.outPacket.setFlag("ACK",True)
                return True
            else: return False # if else, then the 1st handshake is not done right so ignore
        # the following elif succeeds if a valid 3rd handshake is received, so transmission can begin
        elif self.inPacket.getSegment("SEQ") == 135 and self.inPacket.getSegment("ACK") == 90 and not self.inPacket.getFlag("SYN") and self.inPacket.getFlag("ACK"):
            self.connecting = False # the connection has been established
            return True
        else:
            print('********3rd handshake**********')
        return "hey"


    ''' inWindow inserts the packet into the deque
          - returns False if the window is full, True if inserted '''
    def inWindow(self):
        self.windowDeque.append(copy.deepcopy(self.outPacket.packet()))
        return True

    def canSend(self):
        if len(self.windowDeque) == self.windowNum:
            return False
        return True

    def restartWindow(self) -> None:
        self.windowDeque.clear()
        self.timeDeque.clear()

    ''' run when the EXPECTED ack is received
        it adjusts the timeout period '''
    def ackTime(self):
        self.srtt = timer() - self.timeDeque.popleft()
        self.ertt = 0.875*self.ertt + 0.125*self.srtt
        self.tsm = 0.75*self.tsm + 0.25*abs(self.srtt-self.ertt)
        self.toi = self.ertt + 4*self.tsm

    def sendDataPacket(self,_data):
        if len(self.windowDeque) == 0:
            self.timer = time() + self.toi
        self.timeDeque.append(self.timer - self.toi)
