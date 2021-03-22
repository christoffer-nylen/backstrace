# backstrace
Searches for PATTERNS in each file that was opened by a traced process, by analyzing the output from [strace](https://man7.org/linux/man-pages/man1/strace.1.html). 

The primary goals of `backstrace` are:
* Identify files that was recently opened by a process - that might explain an unexpected program exit.
* Identify patterns in files that was recently opened by a process - that might explain an unexpected program exit.

Notes:
* `strace` must be executed with the `-ttt` format option, so the results can be presented in a timely order.
* PATTERNS are interpreted as basic regular expressions (the default option when using `grep`).

## Examples

When user get a build error:
```
$ make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`
```

..the user can use `strace` together with `backstrace` to search all opened files for patterns:

```
$ strace -ttt -f -o strace.log make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`

$ backstrace strace.log Foo_Type
../../../types/ci/ci_dark/my_ctrl_types.hpp:58:struct Foo_Type {
src/my_ctrl/my_ctrl.cpp:46: *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type *ctrls);
src/my_ctrl/my_ctrl.cpp:43:           *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type
src/my_ctrl/my_ctrl.cpp:85:                          Dark_Mode_Setting
```

## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]

## Implementation

The [pystrace](https://github.com/dirtyharrycallahan/pystrace) project is used to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) is used for searching and presenting the lines that match a pattern.
