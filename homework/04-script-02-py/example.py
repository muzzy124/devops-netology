#!/usr/bin/env python3

import os

bash_command = ["git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.getcwd()+'\\'+result.replace('\tmodified:   ', '')
        print(prepare_result)
        #break