from pathlib import Path
from functools import partial
import timeit




''' yield file bytes in 32 byte chunks '''
def fileIter(path):
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read, 32)
        fiterator = iter(reader, bytes())
        for section in fiterator:
            for byt in section:
                yield byt
'''
fileBytes = list(fileIter('testfile.jpeg'))
fileBytes = bytearray(fileBytes)
#print(fileBytes[:50])
#print(fileBytes[:20])

a = bytes(fileBytes[:100])
print(a)
'''
