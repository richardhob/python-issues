# Class Docs (from python/cpython/Lib/timeit.py)

``` python
class Timer:
    """Class for timing execution speed of small code snippets.

    The constructor takes a statement to be timed, an additional
    statement used for setup, and a timer function.  Both statements
    default to 'pass'; the timer function is platform-dependent (see
    module doc string).  If 'globals' is specified, the code will be
    executed within that namespace (as opposed to inside timeit's
    namespace).

    To measure the execution time of the first statement, use the
    timeit() method.  The repeat() method is a convenience to call
    timeit() multiple times and return a list of results.

    The statements may contain newlines, as long as they don't contain
    multi-line string literals.
    """

    def __init__(self, stmt="pass", setup="pass", timer=default_timer,
                 globals=None):
        """Constructor.  See class doc string."""
```

## Timer doc (from python/Doc/library/timeit.rst)


``` rst
.. class:: Timer(stmt='pass', setup='pass', timer=<timer function>, globals=None)

   Class for timing execution speed of small code snippets.

   The constructor takes a statement to be timed, an additional statement used
   for setup, and a timer function.  Both statements default to ``'pass'``;
   the timer function is platform-dependent (see the module doc string).
   *stmt* and *setup* may also contain multiple statements separated by ``;``
   or newlines, as long as they don't contain multi-line string literals.  The
   statement will by default be executed within timeit's namespace; this behavior
   can be controlled by passing a namespace to *globals*.

   To measure the execution time of the first statement, use the :meth:`.timeit`
   method.  The :meth:`.repeat` and :meth:`.autorange` methods are convenience
   methods to call :meth:`.timeit` multiple times.

   The execution time of *setup* is excluded from the overall timed execution run.

   The *stmt* and *setup* parameters can also take objects that are callable
   without arguments.  This will embed calls to them in a timer function that
   will then be executed by :meth:`.timeit`.  Note that the timing overhead is a
   little larger in this case because of the extra function calls.

   .. versionchanged:: 3.5
      The optional *globals* parameter was added.

   .. method:: Timer.timeit(number=1000000)

      Time *number* executions of the main statement.  This executes the setup
      statement once, and then returns the time it takes to execute the main
      statement a number of times.  The default timer returns seconds as a float.
      The argument is the number of times through the loop, defaulting to one
      million.  The main statement, the setup statement and the timer function
      to be used are passed to the constructor.

      .. note::

         By default, :meth:`.timeit` temporarily turns off :term:`garbage
         collection` during the timing.  The advantage of this approach is that
         it makes independent timings more comparable.  The disadvantage is
         that GC may be an important component of the performance of the
         function being measured.  If so, GC can be re-enabled as the first
         statement in the *setup* string.  For example::

            timeit.Timer('for i in range(10): oct(i)', 'gc.enable()').timeit()


   .. method:: Timer.autorange(callback=None)

      Automatically determine how many times to call :meth:`.timeit`.

      This is a convenience function that calls :meth:`.timeit` repeatedly
      so that the total time >= 0.2 second, returning the eventual
      (number of loops, time taken for that number of loops). It calls
      :meth:`.timeit` with increasing numbers from the sequence 1, 2, 5,
      10, 20, 50, ... until the time taken is at least 0.2 second.

      If *callback* is given and is not ``None``, it will be called after
      each trial with two arguments: ``callback(number, time_taken)``.

      .. versionadded:: 3.6


   .. method:: Timer.repeat(repeat=5, number=1000000)

      Call :meth:`.timeit` a few times.

      This is a convenience function that calls the :meth:`.timeit` repeatedly,
      returning a list of results.  The first argument specifies how many times
      to call :meth:`.timeit`.  The second argument specifies the *number*
      argument for :meth:`.timeit`.

      .. note::

         It's tempting to calculate mean and standard deviation from the result
         vector and report these.  However, this is not very useful.
         In a typical case, the lowest value gives a lower bound for how fast
         your machine can run the given code snippet; higher values in the
         result vector are typically not caused by variability in Python's
         speed, but by other processes interfering with your timing accuracy.
         So the :func:`min` of the result is probably the only number you
         should be interested in.  After that, you should look at the entire
         vector and apply common sense rather than statistics.

      .. versionchanged:: 3.7
         Default value of *repeat* changed from 3 to 5.


   .. method:: Timer.print_exc(file=None)

      Helper to print a traceback from the timed code.

      Typical use::

         t = Timer(...)       # outside the try/except
         try:
             t.timeit(...)    # or t.repeat(...)
         except Exception:
             t.print_exc()

      The advantage over the standard traceback is that source lines in the
      compiled template will be displayed.  The optional *file* argument directs
      where the traceback is sent; it defaults to :data:`sys.stderr`.
```

## Patch 

``` diff
diff -r dc0498f4d68e Doc/library/timeit.rst
--- a/Doc/library/timeit.rst	Mon Sep 13 18:45:02 2010 +0200
+++ b/Doc/library/timeit.rst	Mon Sep 13 19:21:09 2010 +0200
@@ -22,25 +22,27 @@
 
 .. class:: Timer([stmt='pass' [, setup='pass' [, timer=<timer function>]]])
 
-   Class for timing execution speed of small code snippets.
+   Class for timing execution speed of small code snippets. The constructor creates 
+   a function that executes the *setup* statement once and then times some number of 
+   executions of the *stmt* statement (see :meth:`Timer.timeit`). Both statements 
+   default to ``'pass'``. The *timer* parameter defaults to a platform-dependent 
+   timer function (see the module doc string). Both *stmt* and *setup* may contain 
+   multiple statements separated by ``;`` or newlines as long as they donâ€™t contain 
+   multi-line string literals.
 
-   The constructor takes a statement to be timed, an additional statement used for
-   setup, and a timer function.  Both statements default to ``'pass'``; the timer
-   function is platform-dependent (see the module doc string).  *stmt* and *setup*
-   may also contain multiple statements separated by ``;`` or newlines, as long as
-   they don't contain multi-line string literals.
+   Both *stmt* and *setup* can also be objects that are callable without arguments. 
+   Passing ``testfunc`` rather than ``'testfunc()'`` may reduce the timing overhead. 
+   However, if ``testfunc`` is a Python function, passing its quoted code should have 
+   even less overhead because doing so eliminates an extra function call.
 
-   To measure the execution time of the first statement, use the :meth:`timeit`
-   method.  The :meth:`repeat` method is a convenience to call :meth:`timeit`
+   To give *stmt* (whether it is a callable name or code string) access to 
+   pre-defined user objects, such as ``testfunc``, *setup* must include an import, 
+   such as ``from __main__ import testfunc``.
+
+   To measure the execution time of *stmt*, use the :meth:`Timer.timeit()` method. 
+   The :meth:`Timer.repeat()` method is a convenience to call :meth:`Timer.timeit()` 
    multiple times and return a list of results.
 
-   .. versionchanged:: 2.6
-      The *stmt* and *setup* parameters can now also take objects that are callable
-      without arguments. This will embed calls to them in a timer function that will
-      then be executed by :meth:`timeit`.  Note that the timing overhead is a little
-      larger in this case because of the extra function calls.
-
-
 .. method:: Timer.print_exc([file=None])
 
    Helper to print a traceback from the timed code.

```

## Update to Doc

``` rst
.. class:: Timer(stmt='pass', setup='pass', timer=<timer function>, globals=None)
 
   Class for timing execution speed of small code snippets.  A Timeit instance
   will contain a function (see :meth:`Timer.timeit`) that executes a snippet of
   *setup* code once and then times some number of executions of *stmt* code. The
   code snippets, given as arguments *setup* and *stmt* when creating the
   instance, may be either strings or callable objects.

   If *setup* or *stmt* is provided as a string, it may contain a python
   expression, statement, or multiple statements separated by ";" or newlines.
   Whitespace adhering to the usual Python indentation rules must follow any
   newlines.

   If *setup* or *stmt* is a callable object, (often a function), the object is
   called with no arguments. Note that the timing overhead is a little larger in
   this case because of the extra function calls required.

   The *setup* and *stmt* parameters default to 'pass'. The *timer* parameter
   defaults to a platform-dependent timer function (see the module doc string).

   When *setup* and *stmt* are run, they are run in a different namespace than
   that of the code that calls :meth:`Timer.timeit()`. To give *stmt* (whether it
   is a callable name or code string) access to objects defined in the code that
   calls timeit, *setup* can import any needed objects. For example, if your code
   defines function ``testfunc()``, *setup* can contain, ``from __main__ import
   testfunc``, and code in *stmt* can then call ``testfunc``.

   To measure the execution time of *stmt*, use the :meth:`Timer.timeit()` method.
   The :meth:`Timer.repeat()` method is a convenience to call :meth:`Timer.timeit()`
   multiple times and return a list of results.


   .. method:: Timer.timeit(number=1000000)

      Time *number* executions of the main snippet. This executes the setup
      snippet once, and then returns the time it takes to execute the main
      snippet a number of times. The default timer returns seconds as a float.
      The argument is the number of times through the loop, defaulting to one
      million. The main snippet, the setup snippet and the timer function
      to be used are passed to the constructor.

      .. note::

         By default, :meth:`.timeit` temporarily turns off :term:`garbage
         collection` during the timing. The advantage of this approach is that
         it makes independent timings more comparable. The disadvantage is
         that GC may be an important component of the performance of the
         function being measured. If so, GC can be re-enabled as the first
         snippet in the *setup* string. For example::

            timeit.Timer('for i in range(10): oct(i)', 'gc.enable()').timeit()

```
