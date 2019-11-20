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
        ''' order of flags in __flags is inportant. Ex: flag in __flags[0] is the 1st bit, and so on '''
        self.__flags = ["FIN","***PUT OTHER FLAGS HERE***"] # put more flags in this list


    def header(self) -> bytearray:
        return self.__header

    ''' set a segment '''
    ''' used for all segments EXCEPT flags, data, and sha256'''
    ''' segment ex: "ACK", or "LENGTH", or "SHA" '''
    ''' value ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value: int) -> None:
        if type(segment) != str:
            raise Exception(f'Provided segment label \"{segment}\" is of type {type(segment)}. It must be of type {type("a")}.')
        segment = segment.upper()
        ''' segment must be valid '''
        if segment not in ["SEQ","ACK","LENGTH","WINDOW"]:
            raise Exception(f'\"{segment}\" is not a valid segment for setSegment().')
        if value >= 2**(8*self.__sizes[segment]) | value < 0:
            #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
            raise Exception(f'Invalid value for {segment}. Must be int between 0 and {self.__sizes[segment]}. Aborting execution of Header.setSegment()')

        for b, i in zip(range(self.__offsets[segment], self.__offsets[segment]+self.__sizes[segment]), range(0, 9**9)):
            ''' convert num to bytes object '''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.__sizes[segment], "big")
            self.__header[b] = bstr[i]

    ''' value must be True or False '''
    def setFlag(self, flag: str, value: bool) -> None:
        if type(flag) != str:
            raise Exception(f'Provided flag label \"{flag}\" is of type {type(flag)}. It must be of type {type("a")}.')
        flag = flag.upper()
        ''' segment must be valid '''
        if flag not in ["FIN"]:
            raise Exception(f'\"{flag}\" is not a valid flag.')
        elif flag not in ["FIN"]:
            raise Exception(f'\"{flag}\" cannot be set using Header.setFlag(). Aborting execution of Header.setFlag()')
        ''' constrain value to what's required for segment '''
        if not isinstance(value, (int, bool)):
            #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
            raise Exception(f'Invalid value for {flag}. Must be boolean. Aborting execution of Header.setFlag()')
        if not (0 <= value <= 1):
            print(f'Caution: value {value} in Header.setFlag automatically interpretted as {bool(value)}.')




        b = self.__header[self.__offsets["FLAGS"]]
        return b






a = Header()

#a.set("ACK",214764870)
try:
    a.setFlag("fin",2)
except Exception as e:
    print(e)

print(a.header())
'''
z = bytes([a.setFlag(1,1)])
print(z)
print(type(z))
'''
