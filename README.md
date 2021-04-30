# backstrace (bs)
Searches for PATTERNS in each file that was opened by a process, by analyzing [strace](https://man7.org/linux/man-pages/man1/strace.1.html) output.

This can be helpful when searching for some definition or symbol that was thrown in a compile error, traceback or exception message from a faulty program or failing build system.

Internally, [pystrace](https://github.com/dirtyharrycallahan/pystrace) is used to parse the strace log, and [grep](https://man7.org/linux/man-pages/man1/grep.1.html) is used for searching and presenting the lines that match a pattern.

## Example

Build failure:
```
$ make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`
```

Use `strace` together with `bs` to search used files for patterns that are related to the failure:

```
$ strace -ttt -f -o strace.log make
src/my_ctrl/my_ctrl.cpp:85: error: ´struct CI::CI_Dark::CI_Dark_Ctrl::Foo_Type´ has no member named `Dark_Mode_Setting`

$ bs Foo_Type strace.log
../../../types/ci/ci_dark/my_ctrl_types.hpp:58:struct Foo_Type {
src/my_ctrl/my_ctrl.cpp:46: *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type *ctrls);
src/my_ctrl/my_ctrl.cpp:43:           *dark_ctrl, CI::CI_Dark::CI_Dark_Ctrl::Foo_Type
src/my_ctrl/my_ctrl.cpp:85:                          Dark_Mode_Setting
```

## Limitations

* `strace` must be executed with the `-ttt` format option, so the results can be presented in a timely order.
* PATTERNS are interpreted as basic regular expressions (the default option when using `grep`).
