#!/usr/bin/python2
from __future__ import print_function

import optparse
import os
import os.path
import sys
import subprocess

from strace import *
from strace_utils import *

def run_cmd(bashCmd):
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if len(output) != 0:
        print(output.rstrip('\n'))
        
    # Ugly trick to check if grep found something:
    return ":" in output

def print_entry(entry):
    print("%s %s %s %s %s %s %s %s %s %s %s %s" % (entry.timestamp,
                                                   entry.syscall name,
                                                   entry.category,
                                                   len(entry.syscall_arguments),
                                                   array_safe_get(entry.syscall_arguments, 0),
                                                   array_safe_get(entry.syscall_arguments, 1),
                                                   array_safe_get(entry.syscall_arguments, 2),
                                                   array_safe_get(entry.syscall_arguments, 3),
                                                   array_safe_get(entry.syscall_arguments, 4),
                                                   array_safe_get(entry.syscall_arguments, 5),
                                                   entry.return_value,
                                                   entry.elapsed_time))
                                                   
def main(argv):
    parser = optparse.OptionParser('usage backstrace: [OPTIONS] FILE PATTERN [PATTERN ..]')
    parser.set_description(__doc__.strip())
    parser.add_option('-c', '--no-color',
                      action="store_false",
                      dest="useColor",
                      help="Don't use markers to highlight the matching strings",
                      default=True)
    parser.add_option('-l', '--files-with-matches',
                      action="store_true",
                      dest="printOnlyFilesWithMatches",
                      help="Print only names of FILEs containing matches",
                      default=False)
                      
    (opts, args) = parser.parse_args(argv)
    if not args:
        parser.print_help()
        return 1
        
    if not os.path.exists(args[0]):
        print('Error: path %s does not exist' % args[0])
        return 1
        
    strace_file = args[0]
    f_in = open(strace_file, "r")
    
    strace_stream = StraceInputStream(f_in)
    
    patterns = list()
    
    for arg in args[1:]:
        patterns.append("-e")
        patterns.append(arg)
        
    cmd_begin = ["grep", "-nHiI"]
    
    if opts.printOnlyFilesWithMatches:
        cmd_begin.append("-l")
        
    if opts.useColor:
        cmd_begin.append("--color=always")
        
    cmd_begin.extend(patterns)
    
    checked_files = set()
    
    linux_dir = ["/bin", "/boot", "/ctxmnt", "/dev", "/lib", "/lib64", "/media", "/mnt", "/opt", "/proc", "/root", "/run", "/sbin", "/srv", "/sw", "/sys", "/usr", "/var", "/x"]
    
    user_dir = []
    
    strace_list = list()
    for entry in strace_stream:
        strace_list.append(entry)
        
    for entry in reversed(strace_list):
        #print_entry(entry)
        if entry.syscall_name == "open":
            filename = array_safe_get(entry.syscall_arguments, 0).strip('\"')
            if not os.access(filename, os.R_OK):
                continue
            if os.path.isdir(filename):
                continue
            if filename.startswith(tuple(linux_dir)):
                continue
            if filename.startswith(tuple(user_dir)):
                continue
            checked_files.add(filename)
            if patterns:
                cmd = list()
                cmd.extend(cmd_begin)
                cmd.append(filename)
                run_cmd(cmd)
            else:
                if opts.printOnlyFilesWithMatches:
                    print(filename)
                else:
                    fin = open(filename, 'r')
                    lines = fin.readlines()
                    for i, line in enumerate(lines):
                        print("%s:%s:%s" % (filename, i, line), end="")
                        
    strace_stream_close()
    
if __name__ == '__main__':
    main(sys.argv[1:])

