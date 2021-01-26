# backstrace
**backstrace** searches for PATTERNS in each file referenced in an [strace](https://man7.org/linux/man-pages/man1/strace.1.html) log.

[grep](https://man7.org/linux/man-pages/man1/grep.1.html) is used to print the lines that matches a pattern. The PATTERNS are interpreted as basic regular expression (the default when using grep).
## Syntax
backstrace [OPTION...] [PATTERN ..] [FILE]
