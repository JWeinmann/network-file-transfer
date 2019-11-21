from pathlib import Path
from functools import partial

''' iterate thru the file '''
def fileIter(path):
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read, 32)
        fiterator = iter(reader, bytes())
        for section in fiterator:
            for byt in section:
                yield byt


''' test file iterator '''
fileBytes = list(fileIter('testfile.jpeg'))
fileBytes = bytearray(fileBytes)
print(fileBytes[-50:]) # just the first 50 bytes
#print(fileBytes[0].to_bytes(1,'big'))
