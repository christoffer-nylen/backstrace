# backstrace
**backstrace** searches for PATTERNS in each file that was opened by a processed traced using [strace](https://man7.org/linux/man-pages/man1/strace.1.html).

It uses [pystrace](https://github.com/dirtyharrycallahan/pystrace) to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) to print the lines that matches a pattern.

backstrace expects the provided strace log to contain timestamps in the "ttt" format so that the matching pattern results can be presented in a timely order. For example, if you would like to analyze the strace of "make", do the following:

```
$ strace -ttt -o make.log make
```

PATTERNS are interpreted as basic regular expressions (default option in grep).

The strace log must be generated with atlease the following options enabled:
* the `OPEN` system call must be logged (default) - to that referenced files can be searched for PATTERNS.
* the `-ttt` option - so that the results can be presented in a correct order.

Example:

Solve buildsystem issues by searching for PATTERNS in files that was accessed during the build process.

In the simplest case strace runs the specified command until it
       exits.  It intercepts and records the system calls which are
       called by a process and the signals which are received by a
       process.  The name of each system call, its arguments and its
       return value are printed on standard error or to the file
       specified with the -o option.

       strace is a useful diagnostic, instructional, and debugging tool.
       System administrators, diagnosticians and trouble-shooters will
       find it invaluable for solving problems with programs for which
       the source is not readily available since they do not need to be
       recompiled in order to trace them.  Students, hackers and the
       overly-curious will find that a great deal can be learned about a
       system and its system calls by tracing even ordinary programs.
       And programmers will find that since system calls and signals are
       events that happen at the user/kernel interface, a close
       examination of this boundary is very useful for bug isolation,
       sanity checking and attempting to capture race conditions.

       Each line in the trace contains the system call name, followed by
       its arguments in parentheses and its return value.  An example
       from stracing the command "cat /dev/null" is:

## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]
