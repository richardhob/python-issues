# 42765: timeit execution environment

## rurpy

library reference manual, section 10.10

The documentation for the timeit module
does not make clear exactly what enviroment
the timed code will be run in, particularly
when a function in the current program is
being timed (as opposed to an external
program.)

This information is available in the examples
section but examples should illustrate already
described behavior, not present new information.

I think the following text should be appended
below the third paragraph in the "class Timer"
section which reads:

To measure the execution time of the first
statement, use the timeit() method. The
repeat() method is a convenience to call
timeit() multiple times and return a list
of results.

Proposed addition:

The timed statement is executed in the namespace
of the timeit module. If a function in the
__main__ module is being timed, it can
be made accessible to the timer module by
using a setup statement like
"from __main__ import xx"
where xx is the function's name in __main__.
Of course "__main__" can be a different module
name if appropriate.

## rhettinger

See related discussion in 

- [bpo-5441](https://bugs.python.org/issue?@action=redirect&bpo=5441) and
- [bpo-2527](https://bugs.python.org/issue?@action=redirect&bpo=2527).

## terryjreedy

I agree that the Timer doc is deficient in not saying that timing is done within a function defined within the timeit module. It is also deficient in not mentioning the secret of how to successfully pass user-defined functions until the very bottom instead of where that option is described. (I had missed this very point until recently.)

The discussion of possible new features for 3.2 (more likely later) does not affect 2.7/3.1 and should not stop a change in 3.2 either. I propose that the Timer doc be revised to the following:

PROPOSED REPLACEMENT

```
Class for timing execution speed of small code snippets. The constructor creates a function that executes the *setup* statement once and then times some number of executions of the *stmt* statement (see Timer.timeit). Both statements default to 'pass'. The *timer* parameter defaults to a platform-dependent timer function (see the module doc string). Both *stmt* and *setup* may contain multiple statements separated by ; or newlines as long as they don’t contain multi-line string literals.

Both *stmt* and *setup* can also be objects that are callable without arguments. Passing testfunc rather than 'testfunc()' may reduce the timing overhead. However, if testfunc is a Python function, passing its quoted code should have even less overhead because doing so eliminates an extra function call.

To give *stmt* (whether it is a callable name or code string) access to pre-defined user objects, such as testfunc, *setup* must include an import, such as 'from __main__ import testfunc'. Note that 'from __main__ import *' does not work because * imports are not legal within functions.

To measure the execution time of *stmt*, use the timeit() method. The repeat() method is a convenience to call timeit() multiple times and return a list of results.
```

Note 1. testfunc , 'testfunc()' , and 'from ....' should be marked up as code. Perhaps the first two should be double quoted also, depending of the style convention. What must be clear is the difference between passing an unquoted function name and a string.

Note 2. The 'may reduce' comment: timeit.timeit(str) (for instance) runs noticeably faster than timeit.timeit('str()'). I presume this is because callables get bound to a local name and local name lookup is faster than builtin lookup. This difference does not apply to imported user names. The existing statement "Note that the timing overhead is a little larger in this case because of the extra function calls." is confusing to me because it does not specify the alternative to 'this case' and there are two possibilities, which I specified.

Note 3. The comment about \* imports should be deleted for 2.7 version.

ADDITIONAL CHANGE

Add the following to the very bottom as part of the final example:

``` python
t = Timer(test, "from __main__ import test")
print(t.timeit()) # should be nearly the same
```

## elibendersky

Terry,

I'm attaching a patch for 2.7, however it's more proof-of-concept than final, because I have a few comments. The patch generally implements your documentation suggestion without the import * warning and without adding the final example. The latter for a couple of reasons:

    My tests show that passing the callable instead of the string 'test()' actually takes longer to run.

    When the callable is passed, the setup of importing 'test' from '__main__' is necessary, because the timed code doesn't have to lookup the 'test' symbol. If you want to leave that example in, the setup string can be ditched.

Let me know your thoughts and I will update the patch.

Attached: [referenced_patch.patch](referenced_patch.patch)

## rurpy2



I find the changes suggested by T Reedy and refined in the
patch by E Bendersky an improvement. However, I found the
following things confused me when reading it:

"...constructor creates a function..."
the constructor creates a Timeit instance, not a function.
There is a method on that instance that is the function but
the way it is phrased in like describing the autos coming off
a Ford production line as "steering wheels". As written, the
statement creates an immediate WTF reaction in my mind.

"...that executes the *setup* statement..."
Use of term "statement" here is confusing as that term already
has a well defined meaning in Python docs. One can't syntactically
use a statement as a function argument. Only by suspending this
confusion and reading further does one discover that "statement"
here means a string containing text of some python code or a
callable object.

Use of "statement" (singular) also directly conflicts with following
information that states multiple statements are ok.

Since the synopsis line already refers to "snippets", I think
continuing to use that is better (having no preexisting conflicting
meanings) than "statement".

"...default to ``'pass'`..."
The call summary immediately above makes clear what the default
parameter values are. While fine to repeat it in text, it is not
high priority information so should be moved to later in the
description.

"...or newlines as long as they donâ€™t contain multi-line string literals..."
What is a multi-line string literal? The Language Reference ->
Lexical Analysis -> String Literals section says nothing about
"multi-line literals".
Is it "a\nb"? Or """a
b"""? Both?
'"a\nb"' actually works. '"""a
b"""' doesn't of course but it is it is also clearly not valid
python string syntax so I'm not sure that 'multi-line strings need
even be mentioned. If it is mentioned then it should be made clear
that multi-line string literals are not allowed not because timeit
doesn't like them, but because python syntax allows no way to
embed them in another string.
.
"...pre-defined user objects..."
What does "pre-defined" mean? Builtin? Imported from stdlib?
I would use a more explicit description here.

I also think a short explanation of *why* one needs to import
program objects in 'setup' makes it a little easier and quicker
to understand what one is doing with the import, particularly if
one is using timeit somewhere other than __main__.. Thus I
suggest expanding that section slightly.

Here is my attempt to adjust taking the above observations into
account. (Sorry, can't supply a patch since I have slow internet
connection and don't have source. Text below is just my hand edit
of the "+" lines in Eli's patch.)

Class for timing execution speed of small code snippets.
A Timeit instance will contain a function (see :meth:`Timer.timeit`)
that executes a snippet of "setup" code once and then times some
number of executions of "stmt" code . The code snippets, given as
arguments *setup* and *stmt* when creating the instance, may be
either strings or callable objects.

If a string, it may contain a python expression, statement, or
multiple statements separated by ";" or newlines. Whitespace
adhering to the usual Python indentation rules must follow any
newlines.

If a callable object, (often a function), the object is called
with no arguments. Note that the timing overhead is a little
larger in this case because of the extra function calls required.

The setup and stmt parameters default to 'pass'.
The timer parameter defaults to a platform-dependent
timer function (see the module doc string).

When the setup and stmt are run, they are run in a
different namespace than that of the code that calls timeit().
To give stmt (whether it is a callable name or code string)
access to objects defined in the code that calls timeit,
setup can import any needed objects. For example, if your
code defines function testfunc(), setup can contain,
from __main__ import testfunc, and code in stmt can
then call testfunc.

To measure the execution time of *stmt*, use the :meth:`Timer.timeit()` method.
The :meth:`Timer.repeat()` method is a convenience to call :meth:`Timer.timeit()`
multiple times and return a list of results.

Changed in version 2.6: The stmt and setup parameters can now
also take objects.

Notes:
----
Added the line "Whitespace adhering..." because when using backslash-n
in strings it is easy to forget about any needed indentation. Sentence
could be deleted if deemed too obvious. There may also be a better
way to phrase it; currently it might imply that some whitespace
is always neccessary if not enough attention paid to the "usual
indentation rules" phrase.

----
In msg116330 - Eli Bendersky (eli.bendersky) wrote:

        My tests show that passing the callable instead of the string
        'test()' actually takes longer to run.

Should the documentation promise that?
I take your word that it also takes longer than running the function's
code directly (outside a function)

The original "Changed in version 2.6" section said

| Note that the timing overhead is a little larger in this case
| [callable objects] because of the extra function calls.

Here, "the other case" is presumably the plain code but could
also be a string function call (e.g. "test()") so I suppose it
is still vacuously true in that case. Accordingly I reused the
statement above in in my suggested changes. Perhaps all three
cases (string code, string function call, callable object)
should be distinguished further and compared re overhead?

## elibendersky

Terry, I'd like to move this forward. New interfaces or not, making the documentation more comprehensible is an important goal in itself.

Could you please comment on rurpy2's latest notes - I will adapt the patch for latest 2.7/3.2/3.3 heads and commit it.
