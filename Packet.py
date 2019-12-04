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

    ''' set a segment '''
    ''' used for 'ACK', 'SEQ', and 'LEN' '''
    ''' value ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value: int) -> None:
        self.setSegExceptions(segment, value)
        for b, i in zip(range(self.offsets[segment], self.offsets[segment]+self.sizes[segment]), range(0, 9**9)):
            ''' convert num to bytes object '''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.sizes[segment], "big")
            self._packet[b] = bstr[i]

    ''' for 'ACK', 'SEQ',or 'LEN' '''
    def getSegment(self, segment: str) -> int:
        if type(segment) != str:
            raise Exception(f'EXCEPTION: Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        if segment not in ["SEQ","ACK","LEN"]:
            raise Exception(f'EXCEPTION: \"{segment}\" is not a valid segment label.')
        seg = bytearray()
        for b, i in zip(range(self.offsets[segment], self.offsets[segment]+self.sizes[segment]), range(0, 9**9)):
            seg.append(self._packet[b])
        return int.from_bytes(bytes(seg),'big')

    ''' value must be True or False '''
    def setFlag(self, flag: str, value: bool) -> None:
        flag = flag.upper() # need to fix this -- upper should not be called until it's verified thru exceptions but it doesn't work if this isn't here
        self.setFlagExceptions(flag, value)
        ''' set or unset flag '''
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
    def shpacket(self, setHash = True):
        sha = hashlib.sha256()
        sha.update(self._packet)
        hash = sha.digest()
        if setHash:
            for b, i in zip(range(self.offsets["SHA"], self.offsets["SHA"]+self.sizes["SHA"]), range(0, 9**9)):
                self._packet[b] = hash[i]
        return hash

    ''' check if the signature is correct '''
    ''' recall: before being sent, the packet is hashed with sha256 with the sha256 segment of the header set to 32 bytes of 0s
        so to check, compare the sha256 segment of the received packet with the hash of the same packet with the sha256 segment cleared '''
    def isgood(self):
        shaOffset = self.offsets["SHA"]
        hash = self._packet[shaOffset:shaOffset+32]
        for b in range(shaOffset, shaOffset+32):
            self._packet[b] = 0
        return hash == self.shpacket(False)



    def setSegExceptions(self, segment: str, value: int) -> None:
        if type(segment) != str:
            raise Exception(f'EXCEPTION: Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        ''' segment must be valid '''
        if segment not in ["SEQ","ACK","LEN"]:
            raise Exception(f'EXCEPTION: \"{segment}\" is not a valid segment label.')
        if value >= 2**(8*self.sizes[segment]) | value < 0:
            raise Exception(f'EXCEPTION: Invalid value for {segment}. Must be int between 0 and {self.sizes[segment]}.')

    def setFlagExceptions(self, flag: str, value: bool) -> None:
        if type(flag) != str:
            raise Exception(f'EXCEPTION: Provided flag label \"{flag}\" is of type {type(flag)}. It must be of type {type("a")}.')
        ''' segment must be valid '''
        if flag not in self.flags:
            raise Exception(f'EXCEPTION: \"{flag}\" is not a valid flag.')
        ''' constrain value to what's required for segment '''
        if not isinstance(value, (int, bool)):
            raise Exception(f'EXCEPTION: Invalid value for {flag}. Must be boolean.')

p = Packet()
print(p._packet)
