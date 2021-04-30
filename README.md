# backstrace
Searches for PATTERNS in each file that was opened by a process, by analyzing output from [strace](https://man7.org/linux/man-pages/man1/strace.1.html). 

The main purpose of the tool is to help with troubleshooting of complex build systems, but it can be used for other purposes as well.

Internally, the [pystrace](https://github.com/dirtyharrycallahan/pystrace) project is used to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) is used for searching and presenting the lines that match a pattern.

## Example

Build failure:
```
$ make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`
```

Use `strace` together with `backstrace` to search used files for patterns that are related to the failure:

```
$ strace -ttt -f -o strace.log make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`

$ backstrace strace.log Foo_Type
../../../types/ci/ci_dark/my_ctrl_types.hpp:58:struct Foo_Type {
src/my_ctrl/my_ctrl.cpp:46: *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type *ctrls);
src/my_ctrl/my_ctrl.cpp:43:           *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type
src/my_ctrl/my_ctrl.cpp:85:                          Dark_Mode_Setting
```

## Limitations

* `strace` must be executed with the `-ttt` format option, so the results can be presented in a timely order.
* PATTERNS are interpreted as basic regular expressions (the default option when using `grep`).
