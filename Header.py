# kill -9 "will be your friend"

'''
going to need to setup some strict limitations on the values for setSegment
'''
class Header:

    def __init__(self) -> None:
        self.__header = __header = bytearray(47)
        ''' offsets for the various sections of the header '''
        self.__offsets = {
            "SEQ": 0,
            "ACK": 4,
            "LENGTH": 8,
            "WINDOW": 10,
            "FLAGS": 12,
            "SHA": 13,
            "DATA": 45
        }
        ''' size of each segment of the header '''
        self.__sizes = {
            "SEQ": 4,
            "ACK": 4,
            "LENGTH": 2,
            "WINDOW": 2,
            "FLAGS": 1,
            "SHA": 32,
            "DATA": 0 # default packet has no data
        }

    def header(self) -> bytearray:
        return self.__header

    ''' set a segment '''
    ''' used for all segments EXCEPT flags, data, and sha256'''
    ''' segment ex: "ACK", or "LENGTH", or "SHA" '''
    ''' value ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value: int) -> None:
        if type(segment) != str:
            raise Exception(f'Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}. Aborting execution of Header.setSegment()')
        ''' segment must be valid '''
        if segment not in ["SEQ","ACK","LENGTH","WINDOW","FLAGS","SHA","DATA"]:
            raise Exception(f'\"{segment}\" is not a valid segment. Aborting execution of Header.setSegment()')
        elif segment in ["FLAGS","SHA","DATA"]:
            raise Exception(f'\"{segment}\" cannot be set using Header.setSegment(). Aborting execution of Header.setSegment()')
        ''' constrain value to what's required for segment '''
        if value >= 2**(8*self.__sizes[segment]) | value < 0:
            #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
            raise Exception(f'Invalid value for {segment}. Must be  between 0 and {self.__sizes[segment]}. Aborting execution of Header.setSegment()')

        for b, i in zip(range(self.__offsets[segment], self.__offsets[segment]+self.__sizes[segment]), range(0, 9**9)):
            ''' convert num to bytes object '''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.__sizes[segment], "big")
            self.__header[b] = bstr[i]

    def setFlag(self, flag: str, value: bool) -> None:
        flag = flag.upper()
        b = self.__header[self.__offsets["FLAGS"]]
        return b






a = Header()

#a.set("ACK",214764870)
try:
    a.setSegment(3,4294967293)
except Exception as e:
    print(e)

print(a.header())
'''
z = bytes([a.setFlag(1,1)])
print(z)
print(type(z))
'''
