# backstrace
**backstrace** searches for PATTERNS in each file that was opened by a process that was traced using [strace](https://man7.org/linux/man-pages/man1/strace.1.html). The tool analyzes an strace FILE where the `-ttt` format has been used and the syscall for `OPEN` has been traced (default).

For example, if you would like to understand which files to start look if you get a cryptic output message from a complex build system.

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

It uses [pystrace](https://github.com/dirtyharrycallahan/pystrace) to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) to print the lines that matches a pattern. PATTERNS are interpreted as basic regular expressions (the default option when using grep). The strace "ttt" format lets the results be presented in a timely order.

## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]
