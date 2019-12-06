import Packet
from collections import deque
from functools import *
import copy
import time
from timeit import default_timer as timer
from FileInteract import getDataChunkList
from concurrent.futures import ThreadPoolExecutor

class Director:

    def __init__(self) -> None:
        self.outPacket = Packet.Packet() # used to build the outgoing packets
        self.inPacket = Packet.Packet() # used to read the incoming packets
        self.scrapPacket = Packet.Packet()
        self.established = False # is True if a connection is established and data transmission should occur
        self.connecting = False # is True if a handshake is/should be occuring
        self.windowNum = 10 # number of windows - will change throughout connection
        self.timer = False # when the first packet in the window expires
        self.dataChunks = getDataChunkList('test.jpeg',1024-45)
        self.chunkPositionHigh = 0 # index of the data chunk in the packet that is highest in the window
        self.chunkPositionLow = 0 # index of the data chunk in the packet that is lowest in the window
        self.lastinACK = 0

    # function below looks at a received packet to see what response (if any) should be made
    # returns bytes if hand-shake, otherwise nothing
    def incoming(self, pkt: bytes):
        self.inPacket.shallowCopy(pkt) # insert the received bytes into the packet class for reading
        self.lastinACK = max(self.lastinACK,self.inPacket.getSegment("ACK"))
        # check if client requests abort
        if self.inPacket.getFlag("RST"):
            self.__init__() # reset the connection
            return
        # checks if there is no connection at all or if there is but it is in the starting hand-shake
        if not self.established or self.connecting:
            return self.openingShake() # always returns False just because no reason
        if self.inPacket.getFlag("FIN"):
            self.__init__() # reset the connection
        return self.processAck()

    # process packet - occurs if connection is fully established and it should just be an ACK
    def processAck(self):
        ackedPos = int((self.inPacket.getSegment("ACK")-180)/1024)-1
        # check if duplicate ACK - if so, replace popped packet and ignore
        if ackedPos < self.chunkPositionLow:
            return
        self.lastinACK = self.inPacket.getSegment("ACK")


        if self.chunkPositionLow == len(self.dataChunks): #last packet was acked, connection can now close
            self.__init__()
            raise Exception("The transfer has completed")
            return
        self.chunkPositionLow = ackedPos + 1
        self.timer = timer() + 0.1
        return

    # called if a packet is received that could potentially be trying to initiate a connecting handshake or complete the 3rd handshake
    def openingShake(self):
        # check if no current connection or hand-shake is occuring (a completely reset connection)
        if not self.established:
            # ensure it's a valid first hand-shake (by this point, that's all it can be)
            if self.inPacket.getSegment("SEQ") == 45 and self.inPacket.getSegment("ACK") == 0 and self.inPacket.getFlag("SYN") and not self.inPacket.getFlag("ACK"):
                self.connecting = True
                self.established = True
                self.outPacket.reset()
                # following 5 lines prepares the response to first hand-shake
                self.outPacket.setSegment("SEQ",90)
                self.outPacket.setSegment("ACK",45)
                self.outPacket.setFlag("ACK",True)
                self.outPacket.setFlag("SYN",True)
                self.outPacket.setSegment("LEN",45)
                return self.outPacket.packet()
            else: return # if else, then the 1st handshake is not done right so ignore
        # the following elif succeeds if a valid 3rd handshake is received, so transmission can begin
        elif self.inPacket.getSegment("SEQ") == 135 and self.inPacket.getSegment("ACK") == 90 and not self.inPacket.getFlag("SYN") and self.inPacket.getFlag("ACK"):
            self.outPacket.reset()
            self.outPacket.setSegment("SEQ",180)
            self.outPacket.setSegment("ACK",135)
            self.outPacket.setFlag("ACK",True)
            self.outPacket.setFlag("SYN",False)
            self.outPacket.setSegment("LEN",45)
            self.connecting = False # the connection has been established
            return self.outPacket.packet()
        return

    # called to send the next data packet
    def trySend(self):
        # make sure connection is entirely established and not in hand-shake
        if not self.established or self.connecting:
            #raise Exception("A full connection has not yet been established, can't send data packets")
            return
        # make sure the low data chunk position hasn't passed the high
        self.chunkPositionHigh = max(self.chunkPositionLow,self.chunkPositionHigh)
        # double check that the transmission hasn't finished yet
        if self.chunkPositionLow == len(self.dataChunks):
            self.__init__()
            raise Exception("The transfer has completed")
            return
        # check to see if window has timed out
        if self.timer and self.timer < timer():
            #print("Window has expired - clearing and resending")
            self.chunkPositionHigh = self.chunkPositionLow
            self.outPacket.reset()
        # check if window is full
        if (self.chunkPositionHigh - self.chunkPositionLow) >= self.windowNum:
            raise Exception("Window full")
            return
        # check if last packet has been sent yet (doesn't necessarily mean the connection is finished though since it might not have received the ack)
        if self.chunkPositionHigh == len(self.dataChunks):
            raise Exception("The last packet has already been sent - just waiting for acknowledgements")
            return
        # **** if all of the above passes then that should mean another packet should be sent containing the data in `dataChunks` at index `chunkPositionHigh`
        self.outPacket.reset()
        ack = 225 + self.chunkPositionHigh * (45 + 1024)
        seq = ack + len(self.dataChunks[self.chunkPositionHigh]) + 45
        self.outPacket.setSegment("ACK",ack)
        self.outPacket.setData(self.dataChunks[self.chunkPositionHigh])
        self.outPacket.setSegment("LEN",len(self.outPacket.packet()))
        self.outPacket.setSegment("SEQ",seq)
        if self.chunkPositionLow == self.chunkPositionHigh:
            self.timer = timer()
        self.chunkPositionHigh = self.chunkPositionHigh + 1
        # check if this is the last packet
        if self.chunkPositionHigh == len(self.dataChunks):
            self.outPacket.setFlag("FIN",True)
        return self.outPacket.packet()

    ''' run when the EXPECTED ack is received it adjusts the timeout period '''
    def ackTime(self):
        return
        '''
        self.srtt = timer() - self.timeDeque.popleft()
        self.ertt = 0.875*self.ertt + 0.125*self.srtt
        self.tsm = 0.75*self.tsm + 0.25*abs(self.srtt-self.ertt)
        self.toi = self.ertt + 4*self.tsm
        '''
