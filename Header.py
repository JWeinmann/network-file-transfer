class Header:

    _header = bytearray(45)

    offsets = {
        "SEQ": 0,
        "ACK": 4,
        "LENGTH": 8,
        "WINDOW": 10,
        "FLAGS": 12,
        "SHA": 13,
        "DATA": 45
    }

    def __init__(self):



        self.__FLAGS = bytes.fromhex('00')

a = Header()

print(a._header)
