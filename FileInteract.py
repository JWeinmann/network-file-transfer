from pathlib import Path
from functools import partial
from collections import deque
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


d = deque(fileIter('testfile.jpeg'))
d = bytearray(d)

#print(d.pop())


fileBytes = list(fileIter('testfile.jpeg'))
#print(fileBytes[:20])
fileBytes = bytearray(fileBytes)
#print(fileBytes[:50])
#print(fileBytes[:20])

a = bytes(fileBytes[:100])
print(a)
