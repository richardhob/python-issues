
# karaken12

Copying a sparse file under Linus using `shutil.copyfile` will not result in a
sparse file at the end of the process. I'm submitting a patch that will remedy
this.

Note that I am only concerned with Linux at the moment -- as far as I know this
patch will not mess things up on other platforms, but this will need to be
tested. It depends on the behavior of `os.truncate()` when the pointer is past
the end of the file, which according to the docs is platform dependant.

Tom

P.S. This is my first time submitting an issue -- if there's anything I need to
do and haven't, please let me know

# bitdancer

You are right that this needs to be tested on other platforms. In order to so
test it (and in any case!), the patch will need unit tests. It also needs doc
updates.

In general patch itself looks good to me, modulo the concern you raise about
truncate. You could move the `'\0'*buflen` constant outside the loop. Also, the
py3k IO module doesn't define constants for 'seek', the docs just refer to the
integers, so it might be best not to use the os constants even though they are
equivalent (the new io module is not a wrapper around os functions the way the
old file implementation was).

FYI, patches should (currently, pending the hg migration) be against the py3k
trunk, and whoever commits it would backport it if appropriate. In this case,
however, it is a new feature and so can only go into py3k trunk.

# pitrou

The use of `fdst.truncate()` is indeed wrong, since `truncate` in 3.x is defined
as truncating up to the current file position (which has been moved forward by
the latest `seek()`)

# karaken12

@pitrou

Hmm... the online docs and th econtents of the doc directory on the trunk branch
say differently

```
Resize the steam to the given *size* in bytes (or the current position if *size*
is not specified). The curretn stream position isn't changed. The resizing can
extend or reduce the current file size. In case of extension, the contents of
the new file area depend on the platform (on most systems, additional bytes are
zero-filled, on Windows they're undetermined). The new file size is returned.
```

Unless you know something else about this, I'm going to assume it's still ok to
use.

@r.david.murray
Thanks for your comments -- I'm trying to put together some unit tests and
documentation, against the Subversion trunk.

Time

# pitrou

Ok, after experimenting, I now understand what the truncate() call is for.

However, your heuristic for detecting sparse files is wrong. The unit for
st_blocks is undefined as per the POSIX standard, although it gives
recommendations:

"The unit for the st_blocks member of the stat structure is not defined within
IEEE Std 1003.1-2001. In some implementations it is 512 bytes. It may differ on
a file system basis. There is no correlation between values of the st_blocks and
st_blksize, and the f_bsize (from <sys/statvfs.h>) structure members.

Traditionally, some implementations defined the multiplier for st_blocks in
<sys/param.h> as the symbol DEV_BSIZE.”

(http://www.opengroup.org/onlinepubs/000095399/basedefs/sys/stat.h.html)

Under Linux, 512 turns out to be the right multiplier (and not st_blksize):

``` python
>>> f = open("foo", "wb")
>>> f.write(b"x" * 4096)
4096
>>> f.truncate(16384)
16384
>>> f.close()
>>> st = os.stat("foo")
>>> st.st_size
16384
>>> st.st_blocks
8
>>> st.st_blocks * st.st_blksize
32768
>>> st.st_blocks * 512
4096
```

Also, GNU `cp` uses `S_BLKSIZE` rather than `DEV_BSIZE` when trying to detect
the `st_blocks` unit size (both are 512 under Linux).

# pitrou

By the way:

> Thanks for your comments -- I'm trying to put together some unit tests > and
> documentation, against the Subversion trunk.

Please ignore trunk; all development (new features) should be done against
branches/py3k.

# SamuelShapiro

Patch fails on CentOS 6 -- python 2.6

```
[root@LG-E1A-LNX python2.6]# patch --dry-run -l -p1 -i shutil-2.6.patch shutil.py
patching file shutil.py
Hunk #1 succeeded at 22 (offset 1 line).
Hunk #2 succeeded at 52 with fuzz 1 (offset 1 line).
Hunk #3 FAILED at 61.
1 out of 3 hunks FAILED -- saving rejects to file shutil.py.rej
```
