import Header

a = Header.Header()

''' test setting segments '''
try:
    a.setSegment("ACK",214764870)
    a.setSegment("SEQ",0x3e426001)
    print(a.header())
except Exception as e:
    print(e)

''' test over-setting segments '''
try:
    a.setSegment("SEQ",0x252525252)
except Exception as e:
    print(e)

''' test wrong segment labels '''
try:
    a.setSegment("abc",52)
except Exception as e:
    print(e)

''' test setting flags '''
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

''' test setting flags with invalid value '''
try:
    a.setFlag("fin","invalid")
except Exception as e:
    print(e)

print(a.header())
