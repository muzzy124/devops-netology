# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.  


    Ответ:
    vagrant@vagrant:~$ strace /bin/bash -c 'cd /tmp'  
    ...  
    chdir("/tmp")                           = 0  
    rt_sigprocmask(SIG_BLOCK, [CHLD], [], 8) = 0  
    rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0  
    exit_group(0)                           = ?  
    +++ exited with 0 +++
    
    таким образом ответ: chdir("/tmp")

2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:
    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
    Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.  

    
    Ответ:
    Запуская strace file /dev/tty, strace file /dev/sda и т.п., в выводе видим, что идет обращение к файлам типа /etc/magic, /home/vagrant/.magic, /usr/share/misc/magic.mgc и т.п.  
    Изучив файлы, понимаем, что база лежит в /usr/share/misc/magic.mgc, при этом просматриваются и прочие файлы *magic*, в которых могут описываться форматы файлов 

3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).


    Ответ:
    запускаем ping 8.8.8.8 > ping.log  
    т.е. команда ping по умолчанию бесконечно возвращает новые и новые строки с результатом пинга, то файл ping.log разрастается в размерах  
    в соседнем терминале удаляем файл ping.log:
    sudo rm ping.log  
    ищем pid процесса:
    pstree -p  
    узнаем pid процесса пинга, например это 1505, далее ищем файловый дескриптор открытого файла ping.log:
    sudo lsof -p 1505 (или sudo lsof -c ping)
      ping    1505 vagrant    1w   REG  253,0    76302 133373 /home/vagrant/ping.log (deleted)  
    отсюда номер дескриптора 1w, т.е. 1
    поэтому открытый файл находится здесь: /proc/1505/fd/1  
    занулить его можно например командой:  
    echo '' | sudo tee /proc/1505/fd/1
    

4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?


    Ответ:  
    Нет. Зомби процесс завершил свое действие, но ещё присутствует в списке процессов операционной системы, чтобы дать родительскому процессу считать код завершения.    

5. В iovisor BCC есть утилита `opensnoop`:
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```
    На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).


    Ответ:
    vagrant@vagrant:~$ sudo opensnoop-bpfcc
      PID    COMM               FD ERR PATH
      1086   vminfo              4   0 /var/run/utmp
      598    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
      598    dbus-daemon        18   0 /usr/share/dbus-1/system-services
      598    dbus-daemon        -1   2 /lib/dbus-1/system-services
      598    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
      612    irqbalance          6   0 /proc/interrupts
      и т.д.

6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.


    Ответ:  
    strace uname -a , отсюда находим системный вызов uname()  
    команда справки по нему "man 2 uname" (2 - системные вызовы)  
    из мануала: Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version,
       domainname}
7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
    ```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
    ```
    Есть ли смысл использовать в bash `&&`, если применить `set -e`?


    Ответ:  
    точка с запятой просто разделяет команды в строке, т.е. запуск команды правее ; не зависит от результата команды левее ;
    && является логическим оператором, при этом запуск команды правее && зависит от успешного результата команды левее &&  

    как указано в help set опция -e  означает немедленный выход, если команда завершается с ненулевым результатом  
    поэтому использование && при установленном set -e не имеет смысла, но && визуально более информативно


8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?


    Ответ:
    e -  немедленный выход, если команда завершается с ненулевым результатом  
    u -  выводит ошибку при использовании неустановленных переменных при замене
    x -  выводит команды и их аргументы по мере их выполнения 
    o pipefail - возвращаемое значение пайплайна есть статус последней команды с ненулевым результатом или ноль, если ни одна команда была завершена с ненулевым результатом  
    таким образом `set -euxo pipefail` подробным образом выводит команды, их аргументф по мере выполнения сценария, а также немедленно прерывает работу при наличии ошибок на любом этапе сценария
9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).


    Ответ:
    из man ps и /process state codes узнаем, что процессы могу быть со статусами:  
      D    uninterruptible sleep (usually IO)
      I    Idle kernel thread
      R    running or runnable (on run queue)
      S    interruptible sleep (waiting for an event to complete)
      T    stopped by job control signal
      t    stopped by debugger during the tracing
      W    paging (not valid since the 2.6.xx kernel)
      X    dead (should never be seen)
      Z    defunct ("zombie") process, terminated but not reaped by its parent
    дополнительные символы означают:  
    For BSD formats and when the stat keyword is used, additional characters may be displayed:
      <    high-priority (not nice to other users)
      N    low-priority (nice to other users)
      L    has pages locked into memory (for real-time and custom IO)
      s    is a session leader
      l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
      +    is in the foreground process group

    анализ количества процессов с тем или иным статусом (например конструкцией типа ps -eo stat | grep ' S' -c) показывает, что больше всего процессов со статусом S и I

      vagrant@vagrant:~$ ps -eo pid,tid,stat,comm
    PID     TID STAT COMMAND
      1       1 Ss   systemd
      2       2 S    kthreadd
      3       3 I<   rcu_gp
      4       4 I<   rcu_par_gp
      6       6 I<   kworker/0:0H-kblockd
      8       8 I<   mm_percpu_wq
      9       9 S    ksoftirqd/0
     10      10 I    rcu_sched
     11      11 S    migration/0
     12      12 S    idle_inject/0
     14      14 S    cpuhp/0
     15      15 S    cpuhp/1
     16      16 S    idle_inject/1
     17      17 S    migration/1
     18      18 S    ksoftirqd/1
     20      20 I<   kworker/1:0H-kblockd
     21      21 S    kdevtmpfs
     22      22 I<   netns
     23      23 S    rcu_tasks_kthre
     24      24 S    kauditd
     25      25 S    khungtaskd
     26      26 S    oom_reaper
     27      27 I<   writeback
     28      28 S    kcompactd0
     29      29 SN   ksmd
     30      30 SN   khugepaged
     77      77 I<   kintegrityd
     78      78 I<   kblockd
     79      79 I<   blkcg_punt_bio
     80      80 I<   tpm_dev_wq
     81      81 I<   ata_sff
     82      82 I<   md
     83      83 I<   edac-poller
     84      84 I<   devfreq_wq
     85      85 S    watchdogd
     88      88 S    kswapd0
     89      89 S    ecryptfs-kthrea
     91      91 I<   kthrotld
     92      92 I<   acpi_thermal_pm
     93      93 S    scsi_eh_0
     94      94 I<   scsi_tmf_0
     95      95 S    scsi_eh_1
     96      96 I<   scsi_tmf_1
     98      98 I<   vfio-irqfd-clea
    100     100 I<   ipv6_addrconf
    109     109 I<   kstrp
    112     112 I<   kworker/u5:0
    125     125 I<   charger_manager
    171     171 S    scsi_eh_2
    172     172 I<   scsi_tmf_2
    190     190 I<   ttm_swap
    191     191 I<   kworker/0:1H-kblockd
    202     202 I<   kdmflush
    203     203 I<   kdmflush
    236     236 I<   raid5wq
    287     287 I<   kworker/1:1H-kblockd
    290     290 S    jbd2/dm-0-8
    291     291 I<   ext4-rsv-conver
    356     356 S<s  systemd-journal
    370     370 I<   rpciod
    372     372 I<   xprtiod
    383     383 Ss   systemd-udevd
    388     388 Ss   systemd-network
    412     412 I<   iprt-VBoxWQueue
    541     541 I<   kaluad
    542     542 I<   kmpath_rdacd
    543     543 I<   kmpathd
    544     544 I<   kmpath_handlerd
    545     545 SLsl multipathd
    576     576 Ss   rpcbind
    577     577 Ss   systemd-resolve
    597     597 Ssl  accounts-daemon
    598     598 Ss   dbus-daemon
    612     612 Ssl  irqbalance
    616     616 Ss   networkd-dispat
    618     618 Ssl  rsyslogd
    627     627 Ss   systemd-logind
    663     663 Ss   cron
    664     664 Ssl  polkitd
    668     668 Ss   atd
    670     670 Ss   sshd
    687     687 Ss+  agetty
    1086    1086 Sl   VBoxService
    1113    1113 Ss   sshd
    1116    1116 Ss   systemd
    1117    1117 S    (sd-pam)
    1150    1150 S    sshd
    1151    1151 Ss   bash
    3979    3979 I    kworker/1:2-events
    4108    4108 I    kworker/u4:2-events_power_efficient
    4234    4234 I    kworker/0:0-events
    4309    4309 I    kworker/0:1
    4311    4311 I    kworker/1:1-events
    4312    4312 Ss   sshd
    4352    4352 S    sshd
    4353    4353 Ss   bash
    4385    4385 I    kworker/u4:0-events_power_efficient
    4453    4453 S+   ping
    4509    4509 I    kworker/u4:3-events_power_efficient
    4587    4587 R    kworker/u4:1-events_unbound
    4597    4597 R+   ps  
    vagrant@vagrant:~$ ps -eo pid,tid,stat,comm | grep S -c
    54
    и т.д.  