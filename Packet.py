import hashlib
import copy

''' Packet is the low-level manipulator/reader of packet bytes '''

class Packet:

    headerSize = 45

    ''' offsets for the various sections of the header '''
    offsets = {
        "SEQ": 0,
        "ACK": 4,
        "LEN": 8,
        "FLAGS": 12,
        "SHA": 13,
        "DATA": 45
    }
    ''' size of each segment of the header '''
    sizes = {
        "SEQ": 4,
        "ACK": 4,
        "LEN": 4,
        "FLAGS": 1,
        "SHA": 32,
    }
    ''' in order from least significant bit to most significant '''
    flags = ["FIN","SYN","ACK", "RST"]

    def __init__(self) -> None:
        self._packet = bytearray(45)

    def packet(self) -> bytearray:
        return self._packet

    def copyPacket(self, pkt) -> None:
        if type(pkt) is bytes:
            self._packet = copy.deepcopy(bytearray(pkt))
            return
        self._packet = copy.deepcopy(pkt)

    def shallowCopy(self, pkt) -> None:
        if type(pkt) is bytes:
            self._packet = bytearray(pkt)
            return
        self._packet = pkt

    ''' set a segment '''
    ''' used for 'ACK', 'SEQ', and 'LEN' '''
    ''' value ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value: int) -> None:
        for b, i in zip(range(self.offsets[segment], self.offsets[segment]+self.sizes[segment]), range(0, 9**9)):
            ''' convert num to bytes object '''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.sizes[segment], "big")
            self._packet[b] = bstr[i]

    ''' for 'ACK', 'SEQ',or 'LEN' '''
    def getSegment(self, segment: str) -> int:
        seg = bytearray()
        for b, i in zip(range(self.offsets[segment], self.offsets[segment]+self.sizes[segment]), range(0, 9**9)):
            seg.append(self._packet[b])
        return int.from_bytes(bytes(seg),'big')

    ''' value must be True or False '''
    def setFlag(self, flag: str, value: bool) -> None:
        if bool(value):
            self._packet[self.offsets["FLAGS"]] = self._packet[self.offsets["FLAGS"]] | (1 << self.flags.index(flag))
        else:
            self._packet[self.offsets["FLAGS"]] = self._packet[self.offsets["FLAGS"]] & ~(1 << self.flags.index(flag))

    ''' print binary of flags segment '''
    def getFlag(self, flag = '' ):
        if not flag:
            #print( 'Flags byte:','{:08b}'.format(self._packet[self.offsets["FLAGS"]]))
            return self._packet[self.offsets["FLAGS"]]
        elif self._packet[self.offsets['FLAGS']] & (1 << self.flags.index(flag.upper())):
            return True
        return False

    def setData(self, dataBytes: bytearray) -> None:
        del self._packet[45:] #remove data
        for b in dataBytes:
            self._packet.append(b)

    ''' fill the SHA segment with the sha256 hash of the entire packet '''
    #******** might need to be disabled if not implemented by client
    def shpacket(self, setHash = True):
        sha = hashlib.sha256()
        sha.update(self._packet)
        hash = sha.digest()
        if setHash:
            for b, i in zip(range(self.offsets["SHA"], self.offsets["SHA"]+self.sizes["SHA"]), range(0, 9**9)):
                self._packet[b] = hash[i]
        return hash

    ''' check if the signature is correct '''
    def isgood(self):
        shaOffset = self.offsets["SHA"]
        hash = self._packet[shaOffset:shaOffset+32]
        for b in range(shaOffset, shaOffset+32):
            self._packet[b] = 0
        return True # ************* remove this when client implements sha256 check
        return hash == self.shpacket(False)

    def trimData(self):
        self.__packet = self.__packet[:45]

    def reset(self):
        self.__packet = bytearray(45)

    def summary(self):
        return f'SEQ({self.getSegment("SEQ")}) ACK({self.getSegment("ACK")}) LEN({self.getSegment("LEN")})\nFlags: SYN {True==self.getFlag("SYN")}, ACK {True==self.getFlag("ACK")}, RST {True==self.getFlag("RST")}, FIN {True==self.getFlag("FIN")}\n'
