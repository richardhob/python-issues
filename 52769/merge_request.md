# Summary

This merge request adds an `errors` return value to the `shutil.rmtree`, based on the patch written in the #pycon 2013 sprint by andrewg (with r.david.murray's assistance). I have attempted to add documentation to explain the purpose of the `errors` return value as well.

Example 1: Path that does not exist

``` python
>>> errors = shutil.rmtree('My Pretend Path', ignore_errors=True)
>>> print(errors)
[(<built-in function lstat>, 'My Pretend Path', FileNotFoundError(2, 'No such file or directory'))]
```

Example 2: Read Only folder with a Read Only File

``` python
>>> errors = shutil.rmtree('ReadOnlyFolder', ignore_errors=True)
>>> print(errors)
[(<built-in function unlink>, 'ReadOnlyFolder/ReadOnlyFile.txt', PermissionError(13, 'Permission denied')), 
 (<built-in function rmdir>, 'ReadOnlyFolder', OSError(39, 'Directory not empty'))]
```

The discussion in this issue revolves around the complexity of the `onerror` function, and what the purpose of the `onerror` (now `onexc`) function is. 

The conclusion from what I read:

- `shutil.rmtree` should not try to delegate the hard work [of removing files and folders, dealing with permissions, etc.] to third party code
- `shutil.rmtree` should return failures / errors, similar to how `smtp` returns a list of mails that could not be sent

Addittional features mentioned that are not implemented but are mentioned:

- `shutil.rmtree` could check to make sure the permissions are the same throught the tree
- `shutil.rmtree` could check and see if there are any links what will make the function fail


