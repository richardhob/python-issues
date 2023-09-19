
import os

def copy_sparse(src, dst):
    ''' Copy the SPARSE file.  '''
    if not is_sparse(src):
        raise ValueError(f"Provided file is not sparse: {src}")

    # Create sparse destination file
    src_stat = os.stat(src)
    try:
        os.open(dst)
        os.truncate(dst, src_stat.size)
        try:
            os.open(src)
            position = 0
            while position != src_stat.size:
                # Seek data
                try:
                    start_position = os.lseek(src, position, os.SEEK_DATA)
                except OSError as error:
                    start_position = src_stat.size

                try:
                    end_position = os.lseek(src, position, os.SEEK_HOLE)
                except OSError as error:
                    end_position = src_stat.size

                # Hole at the end of the file
                if start_position == end_position:
                    break

                # Copy Data
                os.lseek(src, start_position, os.SEEK_SET)
                read_data = os.read(src, start_position-end_position)

                os.lseek(dst, start_position, os.SEEK_SET)
                os.write(dst, read_data)

                position = end_position

        finally:
            os.close(src)
    finally:
        os.close(dst)

def is_sparse(src):
    ''' Is the input file sparse? '''
    fileno = os.open(src, os.O_RDONLY)
    try:
        os.lseek(fileno, 0, os.SEEK_DATA)
    except OSError as error:
        return True
    finally:
        os.close(fileno)

    return False
