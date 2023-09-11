
import os

def sparse(src, dst):
    ''' Copy the SPARSE file.  '''

def is_sparse(src):
    ''' Is the input file sparse? '''
    fileno = os.open(src, os.O_RDONLY)
    try:
        os.lseek(fileno, 0, os.SEEK_DATA)
    except OSError as error:
        return True
    finally:
        os.close(f)

    return False
