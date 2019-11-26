import Packet

a = Packet.Packet()

a.setSegment("ACK",12345)
a.setFlag("SYN",True)
a.setData(b'THIS IS THE DATA')

print(a.packet(),'\n')

b = Packet.Packet()

a.shpacket()

print('A is:\n',a.packet())


b.copyPacket(a.packet())
print('\nB is:\n',b.packet())

print("\nIt's good?")
print(b.isgood())

print("\nB is:")
print(b.packet())

print("\nSetting B's data again")
b.setData(b'THIS IS THE DATA')
print("\nB is:")
print(b.packet())

print("\nIt's good?")
print(b.isgood())
