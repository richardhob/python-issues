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


