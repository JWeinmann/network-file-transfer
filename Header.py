''' Header will be used to modify and read packets Headers '''
''' Another class (perhaps a Connection class or other) will use logic to
determine what the values should be and then will use this to build it '''

class Header:

    ''' can probably clean this up using tuples '''
    def __init__(self) -> None:
        self.__header = bytearray(45)
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
            "DATA": 0 # default packet has no data
        }
        ''' in order from least significant bit to most significant '''
        self.__flags = ["FIN","SYN","ACK", "RST"]

    def header(self) -> bytearray:
        return self.__header

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
            self.__header[b] = bstr[i]

    def getSegment(self, segment: str) -> int:
        #self.getSegExceptions(segment)
        seg = bytearray()
        for b, i in zip(range(self.__offsets[segment], self.__offsets[segment]+self.__sizes[segment]), range(0, 9**9)):
            seg.append(self.__header[b])
        return int.from_bytes(bytes(seg),'big')

    ''' value must be True or False '''
    def setFlag(self, flag: str, value: bool) -> None:
        flag = flag.upper() # need to fix this -- upper should not be called until it's verified thru exceptions
        self.setFlagExceptions(flag, value)
        ''' set or unset flag '''
        if bool(value):
            self.__header[self.__offsets["FLAGS"]] = self.__header[self.__offsets["FLAGS"]] | (1 << self.__flags.index(flag))
        else:
            self.__header[self.__offsets["FLAGS"]] = self.__header[self.__offsets["FLAGS"]] & ~(1 << self.__flags.index(flag))

    ''' print binary of flags segment '''
    ''' *** will need to set some constraints *** '''
    def getFlag(self, flag = '' ):
        if not flag:
            print( 'Flags byte:','{:08b}'.format(self.__header[self.__offsets["FLAGS"]]))
        elif self.__header[self.__offsets['FLAGS']] & (1 << self.__flags.index(flag)):
            return True
        return False

    def setSegExceptions(self, segment: str, value: int) -> None:
        if type(segment) != str:
            raise Exception(f'Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        ''' segment must be valid '''
        if segment not in ["SEQ","ACK","LENGTH","WINDOW"]:
            raise Exception(f'\"{segment}\" is not a valid segment for setSegment().')
        if value >= 2**(8*self.__sizes[segment]) | value < 0:
            #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
            raise Exception(f'Invalid value for {segment}. Must be int between 0 and {self.__sizes[segment]}.')

    def setFlagExceptions(self, flag: str, value: bool) -> None:
        if type(flag) != str:
            raise Exception(f'Provided flag label \"{flag}\" is of type {type(flag)}. It must be of type {type("a")}.')
        ''' segment must be valid '''
        if flag not in self.__flags:
            raise Exception(f'\"{flag}\" is not a valid flag.')
        ''' constrain value to what's required for segment '''
        if not isinstance(value, (int, bool)):
            #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
            raise Exception(f'Invalid value for {flag}. Must be boolean.')
