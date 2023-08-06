# shutil.rmtree and os.listdir cannot recover on error conditions

- [Original Issue in Python Bug Tracker](https://bugs.python.org/issue8523)
- [Github Issue](https://github.com/python/cpython/issues/52769)

## Context

The `shutil.rmtree` function uses the `os.listdir` function to get the list of items in a directory:

``` python
try:
    names = os.listdir(path)
except os.error, err:
    onerror(os.listdir, path, sys.exc_info())
```

When an error occurs, there is nothing that the `onerror` function can do to fix the problem, since the `names` variable won't be updated.

The `onerror` function is a user provided function to help solve errors in the `shutil.rmtree` function.

## Proposed Solution

