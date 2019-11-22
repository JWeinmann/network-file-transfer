import Packet

a = Packet.Packet()

a.setSegment("ACK",12345)
a.setFlag("SYN",True)
a.setData(b'THIS IS THE DATA')

print(a.packet())

b = a

a.shpacket()

print(a.packet())

b.copyPacket(a.packet())
b.setData(b'THISIS THE DATA')

print(b.sgood())

b.setData(b'THIS IS THE DATA')

print(b.sgood())
