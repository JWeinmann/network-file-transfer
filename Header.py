# kill -9 "will be your friend"

'''
going to need to setup some strict limitations on the values set
'''
class Header:
    ''' raw bytes for header'''
    __header = bytearray(47)

    ''' offsets for the various sections of the header '''
    __offsets = {
        "SEQ": 0,
        "ACK": 4,
        "LENGTH": 8,
        "WINDOW": 10,
        "FLAGS": 14,
        "SHA": 15,
        "DATA": 47
    }

    ''' size of each segment of the header '''
    __sizes = {
        "SEQ": 4,
        "ACK": 4,
        "LENGTH": 2,
        "WINDOW": 3, ''' *********double check this *********** '''
        "FLAGS": 1,
        "SHA": 32,
    }

    #def __init__(self):
        #self.__header =
        #self.__FLAGS = bytes.fromhex('00')

    def header(self) -> bytearray:
        return self.__header

    ''' set a segment '''
    ''' used for all segments EXCEPT flags and data '''
    ''' segment ex: "ACK", or "LENGTH", or "SHA" '''
    ''' value can be an int or hex, ex: 2914, or 0x9a'''
    def setSegment(self, segment: str, value) -> None:
        for b, i in zip(range( self.__offsets[segment], self.__offsets[segment] + self.__sizes[segment]    ), range(0, 9**99)    ):
            ''' need to finish this constraint on lengths '''
            if value > 2**(8*self.__sizes[segment]):
                #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
                raise Exception(f'value {self.__sizes[segment]} too large')

            '''convert num to bytes() object'''
            bstr = bytes(4)
            bstr = (value).to_bytes(self.__sizes[segment], "big")
            self.__header[b] = bstr[i]

    def setFlag(self, flag: bool, value) -> None:
        b = self.__header[self.__offsets["FLAGS"]]
        return b






a = Header()

#a.set("ACK",214764870)
a.setSegment("SEQ",0xabcd1234)

z = bytes(a.setFlag(1,1))
print(z.hex())
