# 54225: shutil.copyfile -- allow sparse copying

- [Issue on Github](https://github.com/python/cpython/issues/54225)

## Details

It looks like this patch got started, but abandoned. This feature is kinda neat,
but there is some complexity across platforms... And there are some issues:

1. No unit tests were written
2. No documentation was updated
3. Patch was not tested on Mac or Windows

So we have a lot of work to do on this one!

- [ ] Learn a bit about sparse files
- [ ] Create some tests that create Sparse files
- [ ] Copy them with `shutil.copyfile` and verify they are no longer sparse (Fail)
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

