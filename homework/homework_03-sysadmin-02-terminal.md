Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"
1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.


    cd меняет рабочую папку шелла, данная команда всегда встроенная  
    если бы она была внешней, то не смогла бы менять параметры окружающей среды текущего сеанса шелла

2. Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l? man grep поможет в ответе на этот вопрос. Ознакомьтесь с документом о других подобных некорректных вариантах использования pipe.


    опция -c или --count дает тот же эффект, что и '| wc -l', т.е. подсчитывает количество найденных строк 

3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?


    systemd с pid 1

4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?


    имеем две сессии:  
    vagrant@vagrant:~$ who  
    vagrant  pts/0        2021-11-20 15:15 (10.0.2.2)  
    vagrant  pts/1        2021-11-20 15:43 (10.0.2.2)  
    vagrant@vagrant:~$ ls  
    123.txt  history  temp  terraform  
    vagrant@vagrant:~$ ls blahblah  (вывод ошибки будет в текущем терминале)  
    ls: cannot access 'blahblah': No such file or directory  
    vagrant@vagrant:~$ ls blahblah 2> /dev/pts/1  
    вывод ошибки последней команды будет отображен в соседнем терминале:  
    vagrant@vagrant:~$ ls: cannot access 'blahblah': No such file or directory

5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.


    vagrant@vagrant:~$ ls  
    123.txt  history  temp  terraform  
    vagrant@vagrant:~$ cat 123.txt  
    test message  
    vagrant@vagrant:~$ cat <123.txt > 1234.txt  
    vagrant@vagrant:~$ cat 1234.txt  
    test message  
    vagrant@vagrant:~$


6. Получится ли вывести находясь в графическом режиме данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?


    получится, если переключиться в контекст tty (например комбинацией типа ctrl-alt-f3 и т.п.)

7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?

bash 5>$1 создает декскриптор с номером 5 и отправляет его в stdout  
echo netology > /proc/$$/fd/5 передаст 'netology' в дескриптор 5, который уже перенаправлен в stdout предыдущей командой  
поэтому результатом выполнения второй команды будет netology:

    vagrant@vagrant:~$ bash 5>&1
    vagrant@vagrant:~$ echo netology > /proc/$$/fd/5
    netology

8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.


    vagrant@vagrant:~$ ls  
    1234.txt  123.txt  history  temp  terraform  
    vagrant@vagrant:~$ cat 12345.txt  
    cat: 12345.txt: No such file or directory  
    vagrant@vagrant:~$ cat 12345.txt 111>&2 2>&1 1>&111 | grep 'No such'  
    cat: 12345.txt: No such file or directory  
    vagrant@vagrant:~$ cat 12345.txt 111>&2 2>&1 1>&111 | grep 'No such' -c  
    1  


где:  
111>&2 - перенаправление дескриптор 111 в stderr  
2>&1  - перенаправление stderr в stdout  
1>&111 - перенаправление stdout в дескриптор 111

9. Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?

вывод переменных окружения, аналогично можно запустить printenv

10. Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe.

man proc, там ищем:

    /proc/[pid]/cmdline
                  This read-only file holds the complete command line for the process, unless the process  is  a  zombie.
                  In  the  latter case, there is nothing in this file: that is, a read on this file will return 0 charac‐
                  ters.  The command-line arguments appear in this file as a set  of  strings  separated  by  null  bytes
                  ('\0'), with a further null byte after the last string.
    полная командная строка процесса (если он только не зомби)  
    например для процесса cron с pid 822
    vagrant@vagrant:~$ sudo cat /proc/822/cmdline
    /usr/sbin/cron-f
    
    /proc/[pid]/exe
                  Under  Linux 2.2 and later, this file is a symbolic link containing the actual pathname of the executed
                  command.  This symbolic link can be dereferenced normally; attempting to open it  will  open  the  exe‐
                  cutable.   You  can  even type /proc/[pid]/exe to run another copy of the same executable that is being
                  run by process [pid].  If the pathname has been unlinked, the symbolic link  will  contain  the  string
                  '(deleted)'  appended  to the original pathname.  In a multithreaded process, the contents of this sym‐
                  bolic link are not  available  if  the  main  thread  has  already  terminated  (typically  by  calling
                  pthread_exit(3)).
    
                  Permission  to dereference or read (readlink(2)) this symbolic link is governed by a ptrace access mode
                  PTRACE_MODE_READ_FSCREDS check; see ptrace(2).
    
                  Under Linux 2.0 and earlier, /proc/[pid]/exe is a pointer to the binary which was executed, and appears
                  as a symbolic link.  A readlink(2) call on this file under Linux 2.0 returns a string in the format:
    
                      [device]:inode
    
                  For example, [0301]:1502 would be inode 1502 on device major 03 (IDE, MFM, etc. drives) minor 01 (first
                  partition on the first drive).
    
                  find(1) with the -inum option can be used to locate the file.
    это файл с символьной ссылкой, содержащей путь к исполняемой команде 

11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo.

cat /proc/cpuinfo | grep sse  
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid
sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d  

делаем вывод, что максимальный набор инструкций sse это **sse4_2**



12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:

vagrant@netology1:~$ ssh localhost 'tty'
not a tty
Почитайте, почему так происходит, и как изменить поведение.

tty выдает имя файла терминала, подключенного к стандартному вводу
команда ssh localhost 'tty' запускает новую ssh сессию и выполняет команду tty вместо логин шелла  
поскольку логин шелл не запускается, то и файл терминала к стандартному вводу не создается, поэтому и выдается сообщение от команды tty, что not a tty  
для решения проблемы нужно принудительно задать создание псевдотерминала при ssh подключении опцией -t  
например ssh -t localhost 'tty'


13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии.

для начала нужно установить параметр /proc/sys/kernel/yama/ptrace_scope в 0 (расширяет возможности дебага при использовании ptrace системы)
причем сделать это можно например таким образом (см. ответ на вопрос 14)
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
(напрямую sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope выдает permission denied по той же причине, что и вопрос 14)
после этого выполняем reptyr id_процесса в новом screen для переноса

14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.

Tee выполняет чтение стандартного потока ввода и записывает его в стандартный поток вывода или файлы.  
Поэтому выполнение sudo tee дает права на запись текущего потоко из echo в файл, доступный только руту.

