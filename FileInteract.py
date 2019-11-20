from pathlib import Path
from functools import partial
''' will need to verify that pathlib and functools are installed on school computers '''


''' iterate thru the file '''
def fileIter(path):
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read, 32)
        fiterator = iter(reader, bytes())
        for section in fiterator:
            for byt in section:
                yield byt
