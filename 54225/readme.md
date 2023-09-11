# 54225: shutil.copyfile -- allow sparse copying

- [Issue on Github](https://github.com/python/cpython/issues/54225)

## References

- [sendfile](https://man.freebsd.org/cgi/man.cgi?sendfile(2))

## Details

It looks like this patch got started, but abandoned. This feature is kinda neat,
but there is some complexity across platforms... And there are some issues:

1. No unit tests were written
2. No documentation was updated
3. Patch was not tested on Mac or Windows

So we have a lot of work to do on this one!

- [X] Learn a bit about sparse files
- [X] Create some tests that create Sparse files
- [X] Copy them with `shutil.copyfile` and verify they are no longer sparse (Fail)
- [ ] Does `sendfile` do sparse files?
- [ ] Update `shutil.copyfile` 
    - [ ] Linux
    - [ ] Windows
    - [ ] Mac? (how do I do this one?)
- [ ] Update unittests
    - [ ] Write tests that fail (develop)
    - [ ] Merge changes from feature branch (feature)
    - [ ] Push
- [ ] Update docs
- [ ] Blurb
- [ ] Merge request

## Where do we put the changes?

In the latest Python code, there's some effort to avoid modifying the
`copyfileobj` code to preserve backwards compatibility. So it's probably a good
idea to do that.

Does `os.sendfile` work with sparse files? `python/Modules/posixmodule.c`? Also
what is `sendfile`?

### Sparse Copy

- Determine if a file is sparse or not
- Determine if the file is sparse and empty or sparse and populated
- Determine where there are holds and where there are data
- Copy data across

Questions:

- Copy Permissions?
- Copy Ownership?
- What does `shutil.copy` actually copy?

I think this will work by:

1. Determine file is Sparse
2. Create new file that is the same size and sparse
3. Copy data using lseek

### Sparse Copy Test

- Create an Empty sparse file, and verify it is copied as expected.
- Create a file with data at the very beginning, the middle, and the end, and verify the copied file has the same size / location of data

# First some reading

Let's start off with some reading. I found the following article:

- [Sparse Files with Python by Barry Warsaw](wefearchange.org/2017/01/sparsefiles.rst.html)

This discusses sparse files, why you would want to copy them, and how you can tell if a file is sparse to begin with. It starts with discussing `st_blocks` from stat, but states that this is not effective across file system types (EXT4 and ZFS return different results for example). Also, that copying a sparse files with Holes can be a bit tricky.

First, Creating a Sparse File:

``` python
>>> import os
>>> from pathlib import Path
>>> sparse = Path('/tmp/sparse')
>>> sparse.touch()
>>> os.truncate(str(sparse), 1024)
```

Number of allocated blocks (EXT4):

``` python
>>> sparse.stat().st_blocks 
0
```

Number of allocated blocks (ZFS):

``` python
>>> sparse.stat().st_blocks 
1
```

Question: Is this OK? Isn't a sparse file just a file in which the allocated blocks less than the total size?

Check if a file is empty using `os.SEEK_DATA` from `lseek`:

``` python

import os
import errno

def is_empty(path):
    with open(path, 'r') as fp:
        try:
            os.lseek(fp.fileno(), 0, os.SEEK_DATA)
        except OSError as error:
            if error.errno != errno.ENXIO: # No OSError subclass for ENXIO
                raise
            # The expected exception occurred, meaning that there is no data in the file, so it's entirely sparse
            return True
    # There is data in the file
    return False
```

The article ends by basically saying, "Do as you will with this information." 

Great.

SO let's check out where these constants are used in Python first (maybe someone already did some work for us).

Constants we care about:

- `SEEK_DATA`
- `SEEK_HOLE`

What is this `lseek` function?

## lseek

So `lseek` is a C function, which can be used to manipulate a file. From help:

``` python
lseek(fd, position, whence, /)
    Set the position of a file descriptor.  Return the new position.

      fd
        An open file descriptor, as returned by os.open().
      position
        Position, interpreted relative to 'whence'.
      whence
        The relative position to seek from. Valid values are:
        - SEEK_SET: seek from the start of the file.
        - SEEK_CUR: seek from the current file position.
        - SEEK_END: seek from the end of the file.

    The return value is the number of bytes relative to the beginning of the file.
```

Not mentioned: `SEEK_DATA` and `SEEK_HOLE`

The `lseek` man page has a good description of all the values:

``` 
       lseek() repositions the file offset of the open file description associated with the file descriptor fd to the argument offset according to
       the directive whence as follows:

       SEEK_SET
              The file offset is set to offset bytes.

       SEEK_CUR
              The file offset is set to its current location plus offset bytes.

       SEEK_END
              The file offset is set to the size of the file plus offset bytes.

       lseek() allows the file offset to be set beyond the end of the file (but this does not change the size of the  file).   If  data  is  later
       written  at this point, subsequent reads of the data in the gap (a "hole") return null bytes ('\0') until data is actually written into the
       gap.

   Seeking file data and holes
       Since version 3.1, Linux supports the following additional values for whence:

       SEEK_DATA
              Adjust the file offset to the next location in the file greater than or equal to offset containing data.  If offset points to  data,
              then the file offset is set to offset.

       SEEK_HOLE
              Adjust  the  file  offset to the next hole in the file greater than or equal to offset.  If offset points into the middle of a hole,
              then the file offset is set to offset.  If there is no hole past offset, then the file offset is adjusted to the  end  of  the  file
              (i.e., there is an implicit hole at the end of any file).
```

We should be able to use a combination of `SEEK_DATA` and `SEEK_HOLE` to accomplish what we want:

``` python
if False == is_sparse(my_file):
    return

# File is sparse
with open(original, 'rb') as my_file:
    with open(my_file, 'rb') as my_copy:
        os.truncate(my_copy, size_of(my_file))

        position = -1
        start_position = 0
        while (start_position != position):
            try:
                position = os.lseek(my_file.fileno(), start_position, os.SEEK_DATA)
            except:
                # No more data
                return

            try:
                end_position = os.lseek(my_file.fileno(), position, os.SEEK_HOLE)
            except:
                # Data is at the end of the file
                end_data = size_of(my_file)

            os.lseek(my_file.fileno(), position, os.SEEK_SET)
            data = my_file.read(end_position - start_position)
            os.lseek(my_copy.fileno(), position, os.SEEK_SET)
            my_copy.write(data)
```

Something like that. Let's make our own `copy_sparse` function
