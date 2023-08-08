

# rubenlm

The code that lists directory contents in rmtree is:

``` python
try:
    names = os.listdir(path)
except os.error, err:
    onerror(os.listdir, path, sys.exc_info())
```

If there is an error there is nothing the "onerror" function can do to fix the problem because the variable "names" will not be updated after the problem is solved in "onerror".

Two possible solutions:

1 - Call os.listdir() again after onerror()

``` python
try:
  names = os.listdir(path)
except os.error, err:
  onerror(os.listdir, path, sys.exc_info())
  names = os.listdir(path)
```

2 - Allow onerror() to return a value and set "names" to that value.

``` python
try:
  names = os.listdir(path)
except os.error, err:
  names = onerror(os.listdir, path, sys.exc_info())
```

# bitdancer

If solution 1 is acceptable in the general case, then I think a better fix would look like this:

``` python
try:
    names = os.listdir(path)
except os.error, err:
    onerror(os.listdir, path, sys.exc_info())
    return
```

That is, this is another case in which we can't continue even if onerror returns. However, onerror is free to correct the problem and then call rmtree. (The danger, of course, is infinite recursion, but I don't think it is our responsibility to protect the author of an onerror handler from that potential mistake.)

By analogy to the other place rmtree returns after an onerror call, the above fix does fix a real bug, regardless of the disposition of the feature request, since currently if onerror returns we get a name error.

# rubenlm

Your solution sounds fine to me.

Currently we don't get a NameError because "names" is set to [] before the "try". What happens is that the "for" is skipped and later rmdir fails with "directory not empty".

# tarekziade

The whole error handling in rmtree strikes me as something that cannot be used efficiently. (see also bpo-7969).

How can you decide in an isolated function, that can be called anywhere in the tree you want to remove, the proper thing to do ? You don't know the global status of what is going on.

I think rmtree() should drop these onerror calls and have two different behaviors:

1/ remove all it can in the tree, and return a list of files it couldn't remove, with the error for each file. The developer can then act upon.

2/ analyze the tree to see if the full removal can be done. If it's possible, it does it, if not, it doesn't do anything and return the problems.

For 2/ a possible way to do it could be to copy in a temporary place files that are being removed and copy them back in place in case a problem occurs. This can be long and space consuming though, for big files and big trees. I am not 100% sure 2/ is really useful though...

# rubenlm

Do you really need the global status? I wrote an onerror that seems to works fine after I modified rmtree with the "return" suggested by r.david.murray. It assumes that:

``` python
if os.listdir fails: the user doesn't have read permissions in the dir;
if os.remove or os.rmdir fails: the user doesn't have write permissions in the dir that contains the file/dir being removed.
```

There are other reasons it can fail (attributes, acl, readonly filesystem, ...) but having access to the global status doesn't seem to be of much help anyway.

I don't like your fix 2/ because it can fail to copy files if you don't have read permissions for the file but have write permissions in the directory (so you can delete the file). Besides, the behaviour doesn't seem useful.

/1 seems ok to me but to make use of the global status it provides the user must write a somewhat complex recovery code.

All in all it seems the current behaviour of having an onerror function is more user friendly.

# tarekziade

>    /1 seems ok to me but to make use of the global status it provides
>    the user must write a somewhat complex recovery code.

The onerror() code you did is as complex as a global function working with a sequence returned by rmtree, since it is used *everywhere* in rmtree, and not only for os.listdir issues. IOW, if you didn't handle other possible failures than os.listdir errors, it will fail if rmtree calls it for other APIs like os.remove, etc..

If we state that onerror() is not used as a fallback in rmtree(), and do whatever it wants to do on its side, in an isolated manner, then I find it simpler that this function works will a list of paths rmtree() failed to removed, at the end of the rmtree() process.

I'd be curious to see your onerror() function btw: if it's here just to silent permission errors, 1/ would make it even simpler: don't deal with the error list returned by rmtree() that's all.

# bitdancer

Well, I don't think removing the current onerror support is a viable option for backward compatibility reasons, so we might as well fix it.

I agree that (2) sounds tricky to get reliably right, while I don't see how (1) is an improvement over onerror. It seems to me that the list is either really a tree, in which case the error handler has to reimplement most of rmtree's logic in order to do a recover, or it is a list of error filepath pairs, in which case the error handler would be in most cases simply be iterating over the list and branching based on the error flag...which is no different than what onerror allows, but onerror doesn't need the loop code. Actually, it's less capable than what onerror allows, since if onerror successfully removes a problem file, rmtree will remove the directory, whereas a (1) style handler will have to have its own error logic for dealing with the successive removals (and the (1) style list will have to be guaranteed to be sorted in the correct bottom up order).

I guess I don't see how knowing the global state (which in this case appears to mean the total list of files and directories where removal failed) is useful very often, if ever. It feels like it is a more complicated API that provides little benefit. Do you have some use cases in mind, Tarek?

On the other hand, it seems to me that a nice improvement to onerror would be for it to accept an object, and call an error-case-specific method for each different error case, perhaps even checking for method existence first and doing its normal error handling for that case if the method isn't defined.

# rubenlm

Here is my current error handler:

``` python
def handleRmtreeError(func, path, exc):
  excvalue = exc[1]
  if excvalue.errno == errno.EACCES:
    if func in (os.rmdir, os.remove):
      parentpath = path.rpartition('/')[0]
      os.chmod(parentpath, stat.S_IRWXU) # 0700
      func(path)
    elif func is os.listdir:
      os.chmod(path, stat.S_IRWXU) # 0700
      rmtree(path=path, ignore_errors=False, onerror=handleRmtreeError)
  else:
      raise
```

Looking back to this code there is an infinite recursion bug if os.chmod fails for some reason in the os.listdir condition. I don't see an easy way to solve this...

# tarekziade

>   Well, I don't think removing the current onerror support is a viable
>   option for backward compatibility reasons,
>   so we might as well fix it.

The options could be deprecated since the new behavior would *return* errors.

>   Do you have some use cases in mind, Tarek?

What I have in mind is robustness and simplicity:

robustness because rmtree() will stop calling third party code that can possibly fail and blow the whole process, while working at removing the tree.

Simplicity because, if it fails at removing some files using the usual os.\* APIs, it will just return these errors.

Having this two phases-process will ensure that rmtree() did all that was possible to remove files.

And as I said previously, I am curious to know what is going to be done in the onerror() function when something fails in rmtree(). I doubt any third-party code will do better.

This statement "I couldn't copy this file, try it yourself" seems doomed to complexity.

If the only use case for onerror() is to silent failures, returning these failures seem quite enough. Ala smtp when you get back a list of mails that couldn't be send: it doesn't ask you to send them by yourself, just informs you.

Now maybe we do miss some APIs to check for a file tree sanity, like:

-    are the permissions the same throughout the tree ?
-    is there any link that will make rmtree() fail ?
-    etc/


# tarekziade

Looking at your example rubenlm, it appears like a case that is missing in rmtree().

You are trying to chmod your tree if a file in there cannot be removed because of the permissions. This sounds like something we need to add in rmtree() directly, for example under a "force_permissions" flag that would handle permission failures by trying to chmod.

I think rmtree() should not try to delegate the hard work to third party code, and should try to handle as much failures as possible,
and just return errors.

# andrewsg

Product of the #pycon 2013 sprint with r.david.murray's assistance. This implements the list of results as per tarek's suggested 1/ behavior in cases where ignore_errors=True. Parameters accepted are not changed; return value is changed from None to an empty list in case of no errors or onerror defined by the user, and to a list of tuples exactly like onerror arguments in the case of ignore_errors=True.

As the ignore_errors=True closure-based implementation was adopted from test_shutil.py code, test_shutil.py is changed in one place to take advantage of the new return value in order to add coverage of the new functionality.

# bitdancer

I think this patch looks good, but it needs a documentation update to go with it. Do you want to work on that, Andrew?

It also seems as though there's no bug that it is practical to fix here, so I'm changing this to a pure enhancement request. If anyone disagrees with that, please describe what you think the appropriate bug fix is, and we can break the enhancement request out into a separate issue.
