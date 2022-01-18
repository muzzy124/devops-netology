#!/usr/bin/env python3

import os
import sys

if len(sys.argv)>=2:
    bash_command = ["cd "+sys.argv[1], "git status"]
else:
    bash_command = ["git status"]

result_os = os.popen(' && '.join(bash_command)).read()

for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd()+'/'+result.replace('\tmodified:   ', '')
        print(prepare_result)

