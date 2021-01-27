# backstrace
**backstrace** searches for PATTERNS in each file that was opened by a traced process. This is achieved by analyzing the output from [strace](https://man7.org/linux/man-pages/man1/strace.1.html). 

The primary goals of `backstrace` are:
* Find recently opened files that might provde hints about a problem.
* Find patterns in recently opened files that might provide hints about a problem.

Example: A trouble-shooter wants to find the cause of a build system failure.

```
$ strace -ttt -o make.log make
Traceback (most recent call last):
  File "build_engine.py", line 42, in <module>
    say('OMG')
  File "build_engine.py", line 13, in say
    print("Checking " + nam)
Exception: '

$ backstrace make.log clever_function
```

Notes:
* **strace** must be executed with the `-ttt` format option, this is needed so that the results can be presented in a timely order.


Notice how backstrace starts looking in the files that:
- was most recently opened. This is good because it increases the likely-hood of looking in a file that caused the crash.
- was opened. This is good because it reduces the number of files that needs to be checked.

## Implementation

It uses [pystrace](https://github.com/dirtyharrycallahan/pystrace) to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) to print the lines that matches a pattern. PATTERNS are interpreted as basic regular expressions (the default option when using grep). The strace '-ttt' format lets the results be presented in a timely order (starting with the most recently opened files).

## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]
