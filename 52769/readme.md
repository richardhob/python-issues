# shutil.rmtree and os.listdir cannot recover on error conditions

- [Original Issue in Python Bug Tracker](https://bugs.python.org/issue8523)
- [Github Issue](https://github.com/python/cpython/issues/52769)
- [Bad Copy of Github Issue](./issue-git.md)
- [Copy of Patch From Original Issue](./rmtree_ignore_errors_returns_list.patch)

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

The solution proposed in the `patch` is to add an error list to the `shutil.rmtree` function:

``` diff
diff -r 406c6fd7e753 Lib/shutil.py
--- a/Lib/shutil.py	Sun Mar 17 21:53:48 2013 -0400
+++ b/Lib/shutil.py	Mon Mar 18 14:58:38 2013 -0700
@@ -436,9 +436,10 @@
     is false and onerror is None, an exception is raised.
 
     """
+    errors = []
     if ignore_errors:
         def onerror(*args):
-            pass
+            errors.append(args)
     elif onerror is None:
         def onerror(*args):
             raise
```

`bitdancer` likes this solution, but it also needs a documentation update.

## Checklist

- [ ] Build latest Python (PASS)
- [ ] Run unittests (PASS)
- [ ] Update shutil tests (FAIL)
- [ ] Update shutil (PASS)
- [ ] Update DOCS
    - [ ] Function Docs
    - [ ] User manual docs
