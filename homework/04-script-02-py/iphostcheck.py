#!/usr/bin/env python3

#добавляем поддержку сокетов и работы со временем для таймаутов
import socket
import time

#формируем начальный список хостов и адресов через dict массив
host_ip_list = {'drive.google.com':'192.168.2.2', 'mail.google.com':'192.168.2.3', 'google.com':'192.168.2.4'}

#бесконечный цикл проверки
while True :
    #цикл по каждому хосту из массива
    for host in host_ip_list:
        #определяем текущий реальный айпи адрес хоста командой gethostbyname
        ip = socket.gethostbyname(host)
        #проверяем, совпадает ли текущий адрес хоста с адресом из массива
        if ip != host_ip_list[host] :
            #при несовпадении выводим ошибку, а также адрес из массива и текущий адрес
            print('ERROR: '+host+' IP mismatch: '+host_ip_list[host]+' - '+ip)
            #перезаписываем в массив текущий адрес хоста
            host_ip_list[host] = ip
        else :
            #при совпадении выводим адрес хоста из массива
            print(host+' - '+host_ip_list[host])
        #таймаут для удобства отображения вывода
        time.sleep(2)


