#!/usr/bin/env python3

import os
#добавляем для работы с параметрами в командной строке
import sys

#проверяем наличие параметра в команде (т.е. длина команды больше или равна 2, т.к. по умолчанию без параметра длина 1)
#при этом перенаправляем вывод ошибок git status в &1, чтобы не мешало в дальнейшем
if len(sys.argv)>=2:
        bash_command = ["cd "+sys.argv[1], "git status 2>&1"]
else:
        bash_command = ["git status 2>&1"]

result_os = os.popen(' && '.join(bash_command)).read()

for result in result_os.split('\n'):
        #проверяем, есть ли git в этой папке
        if result.find('fatal') != -1:
                print('В папке '+sys.argv[1]+' нет GIT репозитория')
        #вывод списка измененных файлов
        if result.find('modified') != -1:
                prepare_result = os.getcwd()+'/'+result.replace('\tmodified:   ', '')
                print(prepare_result)