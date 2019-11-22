''' Packet will be used to modify and read packets '''
''' Another class (perhaps a Connection class or other) will use logic to
determine what the values should be and then will use this to build it '''
import hashlib

class Packet:

    ''' can probably clean this up using tuples '''
    def __init__(self) -> None:
        self.__packet = bytearray(45)
        ''' offsets for the various sections of the header '''
        self.__offsets = {
            "SEQ": 0,
            "ACK": 4,
            "LENGTH": 8,
            "FLAGS": 12,
            "SHA": 13,
            "DATA": 45
        }
        ''' size of each segment of the header '''
        self.__sizes = {
            "SEQ": 4,
            "ACK": 4,
            "LENGTH": 4,
            "FLAGS": 1,
            "SHA": 32,
        }
        ''' in order from least significant bit to most significant '''
        self.__flags = ["FIN","SYN","ACK", "RST"]

    def packet(self) -> bytearray:
        return self.__packet

    def copyPacket(self, pkt) -> None:
        self.__packet = pkt

    ''' set a segment '''
    ''' used for all segments EXCEPT flags, data, and sha256'''
    ''' segment ex: "ACK", or "LENGTH", or "SHA" '''
    ''' value ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value: int) -> None:
        self.setSegExceptions(segment, value)
        for b, i in zip(range(self.__offsets[segment], self.__offsets[segment]+self.__sizes[segment]), range(0, 9**9)):
            ''' convert num to bytes object '''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.__sizes[segment], "big")
            self.__packet[b] = bstr[i]

    def getSegment(self, segment: str) -> int:
        if type(segment) != str:
            raise Exception(f'EXCEPTION: Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        if segment not in ["SEQ","ACK","LENGTH"]:
            raise Exception(f'EXCEPTION: \"{segment}\" is not a valid segment label.')
        seg = bytearray()
        for b, i in zip(range(self.__offsets[segment], self.__offsets[segment]+self.__sizes[segment]), range(0, 9**9)):
            seg.append(self.__packet[b])
        return int.from_bytes(bytes(seg),'big')

    ''' value must be True or False '''
    def setFlag(self, flag: str, value: bool) -> None:
        flag = flag.upper() # need to fix this -- upper should not be called until it's verified thru exceptions but it doesn't work if this isn't here
        self.setFlagExceptions(flag, value)
        ''' set or unset flag '''
        if bool(value):
            self.__packet[self.__offsets["FLAGS"]] = self.__packet[self.__offsets["FLAGS"]] | (1 << self.__flags.index(flag))
        else:
            self.__packet[self.__offsets["FLAGS"]] = self.__packet[self.__offsets["FLAGS"]] & ~(1 << self.__flags.index(flag))

    ''' print binary of flags segment '''
    ''' *** will need to set some constraints *** '''
    def getFlag(self, flag = '' ):
        if not flag:
            print( 'Flags byte:','{:08b}'.format(self.__packet[self.__offsets["FLAGS"]]))
        elif type(flag) != str:
            raise Exception(f'EXCEPTION: \"{flag}\" is not a valid flag label.')
        elif self.__packet[self.__offsets['FLAGS']] & (1 << self.__flags.index(flag.upper())):
            return True
        return False

    def setData(self, dataBytes: bytearray) -> None:
        for b in dataBytes:
            self.__packet.append(b)

    ''' fill the SHA segment with the sha256 hash of the entire packet '''
    def shpacket(self):
        sha = hashlib.sha256()
        sha.update(self.__packet)
        hash = sha.digest()
        for b, i in zip(range(self.__offsets["SHA"], self.__offsets["SHA"]+self.__sizes["SHA"]), range(0, 9**9)):
            self.__packet[b] = hash[i]
        return hash

    ''' check if the signature is correct '''
    ''' recall: before being sent, the packet is hashed with sha256 with the sha256 segment of the header set to 32 bytes of 0s
        so to check, compare the sha256 segment of the received packet with the hash of the same packet with the sha256 segment cleared '''
    def sgood(self):
        shaOffset = self.__offsets["SHA"]
        hash = self.__packet[shaOffset:shaOffset+32]
        for b in range(shaOffset, shaOffset+32):
            self.__packet[b] = 0
        return hash == self.shpacket()



    def setSegExceptions(self, segment: str, value: int) -> None:
        if type(segment) != str:
            raise Exception(f'EXCEPTION: Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        ''' segment must be valid '''
        if segment not in ["SEQ","ACK","LENGTH"]:
            raise Exception(f'EXCEPTION: \"{segment}\" is not a valid segment label.')
        if value >= 2**(8*self.__sizes[segment]) | value < 0:
            raise Exception(f'EXCEPTION: Invalid value for {segment}. Must be int between 0 and {self.__sizes[segment]}.')

    def setFlagExceptions(self, flag: str, value: bool) -> None:
        if type(flag) != str:
            raise Exception(f'EXCEPTION: Provided flag label \"{flag}\" is of type {type(flag)}. It must be of type {type("a")}.')
        ''' segment must be valid '''
        if flag not in self.__flags:
            raise Exception(f'EXCEPTION: \"{flag}\" is not a valid flag.')
        ''' constrain value to what's required for segment '''
        if not isinstance(value, (int, bool)):
            raise Exception(f'EXCEPTION: Invalid value for {flag}. Must be boolean.')
