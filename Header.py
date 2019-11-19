# kill -9 "will be your friend"

import itertools

class Header:

    ''' raw bytes for header'''
    _header = bytearray(45)

    ''' offsets for the various sections of the header '''
    _offsets = {
        "SEQ": 0,
        "ACK": 4,
        "LENGTH": 8,
        "WINDOW": 10,
        "FLAGS": 12,
        "SHA": 13,
        "DATA": 45
    }

    ''' size of each segment of the header '''
    _sizes = {
        "SEQ": 4,
        "ACK": 4,
        "LENGTH": 2,
        "WINDOW": 2, ''' *********double check this *********** '''
        "FLAGS": 1,
        "SHA": 32,
    }

    #def __init__(self):
        #self.__header =
        #self.__FLAGS = bytes.fromhex('00')

    ''' set a segment '''
    ''' segment ex: "ACK", or "LENGTH", or "SHA" '''
    ''' value can be an int or hex, ex: 2914, or 0x9a '''
    def set(self, segment: str, value) -> None:
        for b, i in zip(range( self._offsets[segment], self._offsets[segment] + self._sizes[segment]    ), range(0, 10000000)    ):

            '''convert num to bytes() object'''
            bstr = (value).to_bytes(self._sizes[segment], "big")
            if len(bstr) > self.sizes[segment]:
                #raise: Exception(f"The provided value is {len(bstr)} bytes. The value for {segment} cannot be larger than {self._sizes[segment]} bytes.")
                raise: Exception("The provided value is {} bytes. The value for {} cannot be larger than {} bytes.".format(len(bstr),segment,self._sizes[segment]))
            print(bstr.hex())
            self._header[b] = bstr[i]








a = Header()

a.set("ACK",0xa3)
a.set("SEQ",800023)


print(a._header)
