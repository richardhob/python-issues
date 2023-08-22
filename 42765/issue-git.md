# rurpy

library reference manual, section 10.10

The documentation for the timeit module does not make clear what environment the timed code will be run in, particularly when a function in the current program is being timed (as opposed to an external program).

This information is available in the examles section but examples should illustrate already described behavior, not present new information.

I think the following text should be appended below the third paragraph in the "class Timer" section which reads:

> To measure the execution time of the first statement, use the timeit() method. The repeat() method is a convenience to call timeit() multiple times and return a list of results

Proposed addittion:

> The timed statement is executed in the namespace of the timeit module. If a function in the __main__ module is being timed, it can be made accessible to the timer module using a setup statement like "from __main__ import xx" where xx is the function's name in __main__. Of couce "__main__" can be a different module name if appropriate.

# rhettinger 

See related discussion in:

- [bpo-5441]()
- [bpo-2527]()

# terryjreedy

I agree that the Timer doc 
