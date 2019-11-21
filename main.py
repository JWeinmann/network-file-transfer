import cProfile

import Header



a = Header.Header()

#print(a.header())


#cProfile.run(a.setSegment("ACK",0x2a44))

try:
    a.setSegment("ACK",214764870)
    a.setSegment("SEQ",0x3e426001)
    print(a.header())
except Exception as e:
    print(e)

'''
try:
    a.setSegment("SEQ",0x252525252)
except Exception as e:
    print(e)


try:
    a.setSegment("abc",52)
except Exception as e:
    print(e)


try:
    print('1')
    a.setFlag("fin",True)
    print('2')
    a.getFlag()
    a.setFlag("syn",True)
    a.getFlag()
    a.setFlag("fin",False)
    a.getFlag()
except Exception as e:
    print(e)
'''
