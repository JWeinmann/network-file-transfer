from pathlib import Path
from functools import partial

''' yield file bytes in 32 byte chunks '''
def fileIter(path):
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read, 32)
        fiterator = iter(reader, bytes())
        for section in fiterator:
            for byt in section:
                yield byt

def getDataChunkList(path,chunkSize):
    fileBytes = list(fileIter(path))
    fileChunks = []
    pos = 0
    while len(fileBytes):
        fileChunks.append(fileBytes[:min(chunkSize,len(fileBytes))])
        del fileBytes[:chunkSize]
    return fileChunks





'''
data = getDataChunkList('testfile.jpeg',4096-45)

print(len(data))
print("\n\n\n")
fileBytes = list(fileIter('testfile.jpeg'))
print(fileBytes[-979:])
#print(fileBytes[:20])
'''
