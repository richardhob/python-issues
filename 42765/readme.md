# Timeit execution environment

- [Issue on Github](https://github.com/python/cpython/issues/42765)

## Reference

- [Git Issue Notes](./git_issue.md)

## Overview

The documentation of the `timeit` class is lacking, and can be improved. The issue has a layout of the changes to be made, but it needs some polish. Looks pretty easy to update honestly.

## Plan

- [X] Make a new branch (gh42765-timit-execution-environment)
- [X] Run Tests and record results
- [ ] Create `timeit.md` document with the Timer class docs
- [ ] Add a section in the `timeit.md` with the updated doc
- [ ] Start revising based on feedback in post
- [ ] Run tests
- [ ] Create Merge request

## 2023-08-28 Test Results

``` bash
== Tests result: FAILURE then SUCCESS ==

445 tests OK.

18 tests skipped:
    test.test_asyncio.test_windows_events
    test.test_asyncio.test_windows_utils test_dbm_gnu test_dbm_ndbm
    test_devpoll test_ioctl test_kqueue test_launcher test_lzma
    test_startfile test_tkinter test_ttk test_winconsoleio test_winreg
    test_winsound test_wmi test_zipfile64 test_zoneinfo

1 re-run test:
    test_tools

Total duration: 38 min 44 sec
Tests result: FAILURE then SUCCESS
```

