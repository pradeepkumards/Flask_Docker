#!/usr/bin/python

import os,sys
print sys.argv
action =  sys.argv[1]
if action == 'touch':
    open("testing_file", "w").close()
elif action == 'mkdir':
    os.mkdir("testing_dir")
