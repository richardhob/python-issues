# shutil.rmtree(path, ignore_errors=False, onerror=None, *, onexc=None, dir_fd=None)

Delete an entire directory tree; path must point to a directory (but not a symbolic link to a directory). If ignore_errors is true, errors resulting from failed removals will be ignored; if false or omitted, such errors are handled by calling a handler specified by onexc or onerror or, if both are omitted, exceptions are propagated to the caller.

This function can support [paths relative to directory descriptors](https://docs.python.org/3.12/library/os.html#dir-fd).

.. note:

    On platforms that support the necessary fd-based functions a symlink attack resistant version of rmtree() is used by default. On other platforms, the rmtree() implementation is susceptible to a symlink attack: given proper timing and circumstances, attackers can manipulate symlinks on the filesystem to delete files they wouldn’t be able to access otherwise.  Applications can use the rmtree.avoids_symlink_attacks function attribute to determine which case applies. 

If `onexc` is provided, it must be a callable that accepts three parameters: `function`, `path`, and `excinfo`.

The first parameter, `function`, is the function which raised the exception; it depends on the platform and implementation. The second parameter, `path`, will be the path name passed to function. The third parameter, `excinfo`, is the exception that was raised. Exceptions raised by `onexc` will not be caught.

The deprecated `onerror` is similar to `onexc`, except that the third parameter it receives is the tuple returned from `sys.exc_info()`.

Raises an [auditing event](https://docs.python.org/3.12/library/sys.html#auditing) `shutil.rmtree` with arguments `path`, `dir_fd`.

Changed in version 3.3: Added a symlink attack resistant version that is used automatically if platform supports fd-based functions.

Changed in version 3.8: On Windows, will no longer delete the contents of a directory junction before removing the junction.

Changed in version 3.11: The `dir_fd` parameter.

Changed in version 3.12: Added the onexc parameter, deprecated onerror.

