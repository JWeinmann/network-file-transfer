import Packet


'''
TESTS for Header
'''

a = Packet.Packet()

''' Valid segment changes '''
print("\nTrying valid setSegment calls")
print("\nBEFORE", a.packet())
try:
    a.setSegment("ACK",214764870)
    a.setSegment("SEQ",1234567)
    a.setSegment("LENGTH",718293)
    print('\n***TEST PASSED***')
except Exception as e:
    print(e)
    print("\nTEST FAILED - an Exception shouldn't have occured")
print("\nAFTER", a.packet())


''' invalid segment changes '''
print("\n\nTrying invalid setSegment calls")
try:
    a.setSegment("SEQ",0x252525252) #too big value
    print("TEST PART 1 FAILED - an Exception should have occured")
except Exception as e:
    print(e)
    print('***TEST PART 1 PASSED***')
try:
    a.setSegment("abc",0x252522) #invalid label
    print("TEST PART 2 FAILED - an Exception should have occured")
except Exception as e:
    print(e)
    print('***TEST PART 2 PASSED***')
try:
    a.setSegment(1,0x252522) #invalid label
    print("TEST PART 3 FAILED - an Exception should have occured")
except Exception as e:
    print(e)
    print('***TEST PART 3 PASSED***')

''' Get Segments '''
print("\n\nTrying valid getSegment calls")
try:
    a.getSegment("ACK")
    a.getSegment("SEQ")
    a.getSegment("LENGTH")
    print('***TEST PASSED***')
except Exception as e:
    print(e)
    print("TEST FAILED - an Exception shouldn't have occured")


''' valid set and get flag calls '''
print('\n\nTrying valid flag set and get calls\n')
try:
    print('set FIN to True')
    a.setFlag("fin",True)
    print('get flags')
    a.getFlag()
    print('set SYN to True')
    a.setFlag("syn",True)
    print('get flags')
    a.getFlag()
    print('set FIN to True')
    a.setFlag("fin",False)
    print('get flags')
    a.getFlag()
    print('get specific flag FIN')
    a.getFlag('fin')
    print('get specific flag SYN')
    a.getFlag('SYN')
    print("***TEST PASSED***")
except Exception as e:
    print(e)
    print("TEST FAILED")


''' invalid set and get flag calls '''
print('\n\nTrying invalid flag set and get calls\n')
try:
    print('set ABC to True')
    a.setFlag("abc",True)
    print('TEST PART 1 FAILED - An exception should have occured')
except Exception as e:
    print(e)
    print("***TEST PART 1 PASSED***")
try:
    print('set FIN to \"helloworld\"')
    a.setFlag("FIN","helloworld")
    print('TEST PART 2 FAILED - An exception should have occured')
except Exception as e:
    print(e)
    print("***TEST PART 2 PASSED***")
