# backstrace
Searches for PATTERNS in each file that was opened by a traced process, by analyzing the output from [strace](https://man7.org/linux/man-pages/man1/strace.1.html). 

The primary goals of `backstrace` are:
* Identify recently opened files - that might be causing an unexpected program exit.
* Identify a pattern in recently opened files - that might might provide further hints about an unexpected program exit.

Notes:
* `strace` must be executed with the `-ttt` format option, so that the results can be presented in a timely order.
* PATTERNS are interpreted as basic regular expressions (the default option when using `grep`).

## Examples
Which opened files contains the word `foo`?
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

Which files were opened?
```
$ strace -ttt -o make.log make
Traceback (most recent call last):
  File "build_engine.py", line 42, in <module>
    say('OMG')
  File "build_engine.py", line 13, in say
    print("Checking " + nam)
Exception: '

$ backstrace make.log -l
```

## Implementation

The [pystrace](https://github.com/dirtyharrycallahan/pystrace) project is used to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) is used for searching and presenting the lines that match a pattern.

## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]
