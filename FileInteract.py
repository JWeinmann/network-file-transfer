from pathlib import Path
from functools import partial

''' yield file bytes in 32 byte chunks '''
def fileIter(path):
    path = Path(path)
    return open(path, "rb").read()

def getDataChunkList(path,chunkSize):
    fileBytes = list(fileIter(path))
    fileChunks = [fileBytes[i:i+chunkSize] for i in range(0,len(fileBytes),chunkSize)]
    return fileChunks

'''
Old way
2500 chunks of 1024 bytes were loaded
elapsed time:  1.0290924270000232

New way
2500 chunks of 1024 bytes were loaded
elapsed time:  0.03627903299991431
'''
