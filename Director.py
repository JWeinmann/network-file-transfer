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
        self.finished = False # True is final packet has been sent and just waiting for ACK
        self.established = False # is True if a connection is established and data transmission should occur
        self.connecting = False # is True if a handshake is/should be occuring
        self.windowNum = 100 # number of windows - will change throughout connection
        self.windowDeque = deque() # a queue holding the packets in the window
        self.timeDeque = deque()  # a queue holding the timeout times for each corresponding packet in the window
        self.timer = None # when the first packet in the window expires
        self.toi = 0.001 # time-out interval
        self.srtt = 0.0005 # sample round-trip time - last round-trip time
        self.ertt = 0.0005 # estimated / smoothed rount-trip time
        self.tsm = 0.0005 # time safety margin
        self.dataLocation = 0
        self.dataChunks = [] # list of the chunks of bytes of the file to be sent
        self.dataChunks = getDataChunkList('testfile.jpeg',4096-45)
        self.chunkPositionHigh = 0 # index of the data chunk in the packet that is highest in the window
        self.chunkPositionLow = 0 # index of the data chunk in the packet that is lowest in the window
        self.lastinPacketTime = False
        self.lastinSEQ = 0
        self.lastinACK = 0

    # function below looks at a received packet to see what response (if any) should be made
    # returns bytes if hand-shake, otherwise nothing
    def incoming(self, pkt: bytes):
        self.lastinPacketTime = timer()
        self.inPacket.copyPacket(pkt) # insert the received bytes into the packet class for reading
        self.lastinACK = max(self.lastinACK,self.inPacket.getSegment("ACK"))
        self.lastinSEQ = max(self.lastinSEQ,self.inPacket.getSegment("SEQ"))
        # check if client requests abort
        if self.inPacket.getFlag("RST"):
            self.__init__() # reset the connection
            return
        # checks if there is no connection at all or if there is but it is in the starting hand-shake
        if not self.established or self.connecting:
            return self.openingShake() # always returns False just because no reason
        if self.inPacket.getFlag("FIN") and self.inPacket.getFlag("ACK"):
            self.__init__() # reset the connection
        return self.processAck()

    # process packet - occurs if connection is fully established and it should just be an ACK
    def processAck(self):
        try:
            self.scrapPacket.shallowCopy(self.windowDeque.popleft()) # pop pkt from 1st window for checking
        except IndexError:
            print("Received ACK packet but the Window is empty - there is nothing to acknowledge")
            return
        # check if duplicate ACK - if so, replace popped packet and ignore
        if self.inPacket.getSegment("ACK") < self.scrapPacket.getSegment("SEQ"):
            self.windowDeque.appendleft(self.scrapPacket.packet()) # replace pkt into Window because it's not yet acked
            return
        # check if it's the expected ACK
        elif self.inPacket.getSegment("ACK") == self.scrapPacket.getSegment("SEQ"):
            self.chunkPositionLow = self.chunkPositionLow + 1
            if self.chunkPositionLow == len(self.dataChunks): #last packet was acked, connection can now close
                self.__init__()
                self.finished = True
                raise Exception("The transfer has completed")
                return
            self.ackTime() # this changes the timeout interval for optimization
            try:
                self.timeDeque.popleft() # remove the timeout for the packet just acked
                self.timer = self.timeDeque.popleft() # part of adjusting the timer
            except IndexError:
                print("time deque is unexpectedly empty - something went wrong with syncing the time deque with the window deque")
                return
            # 2 lines below adjust the timer
            self.timeDeque.appendleft(self.timer)
            self.timer = self.timer + self.toi
            return
        # the While loop runs if the received ACK must be for a packet later in the window
        # this occurs if one of the ack packets was dropped but client still received later packets
        while True:
            try:
                self.scrapPacket.shallowCopy(self.windowDeque.popleft())
            except IndexError:
                print("Received an ACK that is higher than anything in the window - something went critically wrong. Aborting connection.")
                # *********** send a RST packet
                self.__init__()
                return
            self.chunkPositionLow = self.chunkPositionLow + 1
            if self.chunkPositionLow == len(self.dataChunks): #last packet was acked, connection can now close
                self.__init__()
                self.finished = True
                raise Exception("The transfer has completed")
                return
            try:
                self.timeDeque.popleft()
            except IndexError:
                print("time deque is unexpectedly empty - something went wrong with syncing the time deque with the window deque")
                return
            if self.inPacket.getSegment("ACK") == self.scrapPacket.getSegment("SEQ"):
                self.chunkPositionLow = self.chunkPositionLow + 1
                if self.chunkPositionLow == len(self.dataChunks): #last packet was acked, connection can now close
                    self.__init__()
                    self.finished = True
                    raise Exception("The transfer has completed")
                    return
                try:
                    self.timeDeque.popleft() # remove the timeout for the packet just acked
                    self.timer = self.timeDeque.popleft()
                except IndexError:
                    print("time deque is unexpectedly empty - something went wrong with syncing the time deque with the window deque")
                    return
                self.timeDeque.appendleft(self.timer)
                self.timer = self.timer + self.toi
                break
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
            self.connecting = False # the connection has been established
            self.outPacket.reset()
            self.outPacket.setSegment("SEQ",180)
            self.outPacket.setSegment("ACK",135)
            self.outPacket.setFlag("ACK",True)
            self.outPacket.setFlag("SYN",False)
            self.outPacket.setSegment("LEN",45)
            return self.outPacket.packet()
        else:
            return
        return

    # called to send the next data packet
    def trySend(self):
        # make sure connection is entirely established and not in hand-shake
        if not self.established or self.connecting:
            raise Exception("A full connection has not yet been established, can't send data packets")
            return
        # check to see if the connection as a whole has timed out
        if not self.lastinPacketTime and (self.lastinPacketTime+10)<timer():
            self.__init__()
            print("Connection has timed out - resetting")
            self.outPacket.setFlag("RST",True)
            return outPacket.packet() # sending a RST packet
        # make sure the low data chunk position hasn't passed the high
        self.chunkPositionHigh = max(self.chunkPositionLow,self.chunkPositionHigh)
        # double check that the transmission hasn't finished yet
        if self.chunkPositionLow == len(self.dataChunks):
            self.__init__()
            raise Exception("The transfer has completed")
            return
        # check to see if window has timed out
        if not self.timer:
            if self.timer < timer():
                print("Window has expired - clearing and resending")
                self.windowDeque.clear()
                self.timeDeque.clear()
                self.chunkPositionHigh = self.chunkPositionLow
                self.outPacket.reset()
        # check if window is full
        if len(self.windowDeque) >= self.windowNum:
            raise Exception("Window full")
            return
        # check if last packet has been sent yet (doesn't necessarily mean the connection is finished though since it might not have received the ack)
        if self.chunkPositionHigh == len(self.dataChunks):
            raise Exception("The last packet has already been sent - just waiting for acknowledgements")
            return

        # **** if all of the above passes then that should mean another packet should be sent containing the data in `dataChunks` at index `chunkPositionHigh`
        self.outPacket.reset()
        self.outPacket.setSegment("ACK",self.lastinSEQ+len(self.windowDeque)*(4096+45))
        self.outPacket.setData(self.dataChunks[self.chunkPositionHigh])
        self.outPacket.setSegment("LEN",len(self.outPacket.packet()))
        if self.outPacket.getSegment("LEN") > 4096:
            self.__init__()
            self.outPacket.reset()
            self.outPacket.setFlag("RST",True)
            raise Exception("Critical error - packet greater than 4096 bytes was somehow built, aborting connection")
            return self.outPacket.packet()
        self.outPacket.setSegment("SEQ",self.outPacket.getSegment("LEN")+self.outPacket.getSegment("ACK"))
        self.chunkPositionHigh = self.chunkPositionHigh + 1
        # check if this is the last packet
        if self.chunkPositionHigh == len(self.dataChunks):
            self.outPacket.setFlag("FIN",True)
        self.windowDeque.append(self.outPacket.packet())
        if not len(self.timeDeque):
            self.timer = timer() + self.toi
        self.timeDeque.append(timer())
        return self.outPacket.packet()

    ''' run when the EXPECTED ack is received it adjusts the timeout period '''
    def ackTime(self):
        self.srtt = timer() - self.timeDeque.popleft()
        self.ertt = 0.875*self.ertt + 0.125*self.srtt
        self.tsm = 0.75*self.tsm + 0.25*abs(self.srtt-self.ertt)
        self.toi = self.ertt + 4*self.tsm
