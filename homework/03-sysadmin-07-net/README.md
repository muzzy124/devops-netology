#Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"
1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?
```
windows: ipconfig или в powershell: Get-NetIPInterface 
PS C:\> Get-NetIPInterface

ifIndex InterfaceAlias                  AddressFamily NlMtu(Bytes) InterfaceMetric Dhcp     ConnectionState PolicyStore
------- --------------                  ------------- ------------ --------------- ----     --------------- -----------
45      vEthernet (WSL)                 IPv6                  1500            5000 Enabled  Connected       ActiveStore
31      vEthernet (Default Switch)      IPv6                  1500            5000 Enabled  Connected       ActiveStore
14      Сетевое подключение Bluetooth   IPv6                  1500              65 Disabled Disconnected    ActiveStore
17      VirtualBox Host-Only Network    IPv6                  1500              25 Enabled  Connected       ActiveStore
4       Radmin VPN                      IPv6                  1500              35 Enabled  Connected       ActiveStore
16      Teredo Tunneling Pseudo-Inte... IPv6                  1280              75 Enabled  Connected       ActiveStore
1       Loopback Pseudo-Interface 1     IPv6            4294967295              75 Disabled Connected       ActiveStore
45      vEthernet (WSL)                 IPv4                  1500            5000 Disabled Connected       ActiveStore
31      vEthernet (Default Switch)      IPv4                  1500            5000 Disabled Connected       ActiveStore
14      Сетевое подключение Bluetooth   IPv4                  1500              65 Enabled  Disconnected    ActiveStore
17      VirtualBox Host-Only Network    IPv4                  1404              25 Disabled Connected       ActiveStore
4       Radmin VPN                      IPv4                  1500               1 Disabled Connected       ActiveStore
19      Ethernet                        IPv4                  1500              25 Disabled Connected       ActiveStore
1       Loopback Pseudo-Interface 1     IPv4            4294967295              75 Disabled Connected       ActiveStore


linux: ip link, ifconfig и т.п.
root@CORE-I7:~# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether e6:9d:02:7f:63:f3 brd ff:ff:ff:ff:ff:ff
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 9e:d4:70:a3:b5:bb brd ff:ff:ff:ff:ff:ff
4: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:15:5d:f7:1e:31 brd ff:ff:ff:ff:ff:ff
5: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/sit 0.0.0.0 brd 0.0.0.0
```
2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?
```
протокол arp
root@CORE-I7:~# ip neighbor
172.21.176.1 dev eth0 lladdr 00:15:5d:ef:97:11 STALE

в ipv6 - ndp (и то фактически он на базе icmpv6)
apt install libndp-tools
ndptools monitor или send

```
3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.
```
vlan
установка  через, например, apt install vlan
(при этом модуль 8021q должен быть включен в ядро)

конфиг можно через ip link vlan (пример с тегом 10 к существующему интерфейсу eth0):
ip link add link eth0 name eth0.10 type vlan id 10

```
4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.
```
в ubuntu нужно включить modprobe bonding
(на старых релизах еще и установить apt-get install ifenslave)

типы бондинга
mode=0 (balance-rr)
mode=1 (active-backup)
mode=2 (balance-xor)
mode=3 (broadcast)
mode=4 (802.3ad)
mode=5 (balance-tlb)
mode=6 (balance-alb)

пример (объединям два физ. интерфейса eth0 и eth1 в бонд типа 4 (802.3ad):
sudo -i
ip link add bond0 type bond mode 802.3ad
ip link set eth0 master bond0
ip link set eth1 master bond0
(только это живет до след. ребута, иначе нужно править конфиг)
```
5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
```
/29 маска дает 8 адресов, из которых первый и последний это сеть и броадкаст, и только 6 хостов
/24 маска дает 256 адресов, таким образом можно получить 256/8=32 сети /29
например
10.10.10.0/29, 10.10.10.9/29, 10.10.10.17/29 и т.п.

root@CORE-I7:/etc/network/if-up.d# subnetcalc 10.10.10.0/29
Address       = 10.10.10.0
                   00001010 . 00001010 . 00001010 . 00000000
Network       = 10.10.10.0 / 29
Netmask       = 255.255.255.248
Broadcast     = 10.10.10.7
Wildcard Mask = 0.0.0.7
Hosts Bits    = 3
Max. Hosts    = 6   (2^3 - 2)
Host Range    = { 10.10.10.1 - 10.10.10.6 }
...
root@CORE-I7:/etc/network/if-up.d# subnetcalc 10.10.10.9/29
Address       = 10.10.10.9
                   00001010 . 00001010 . 00001010 . 00001001
Network       = 10.10.10.8 / 29
Netmask       = 255.255.255.248
Broadcast     = 10.10.10.15
Wildcard Mask = 0.0.0.7
Hosts Bits    = 3
Max. Hosts    = 6   (2^3 - 2)
Host Range    = { 10.10.10.9 - 10.10.10.14 }
...
```
6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.
```
остался только диапазон 100.64.0.0/10, например 100.100.100.0/26

root@CORE-I7:/etc/network/if-up.d# subnetcalc 100.100.100.0/26
Address       = 100.100.100.0
                   01100100 . 01100100 . 01100100 . 00000000
Network       = 100.100.100.0 / 26
Netmask       = 255.255.255.192
Broadcast     = 100.100.100.63
Wildcard Mask = 0.0.0.63
Hosts Bits    = 6
Max. Hosts    = 62   (2^6 - 2)
Host Range    = { 100.100.100.1 - 100.100.100.62 }
...
```
7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?
```
windows:
arp -a - показать текущую таблицу arp (можно еще -v для подробностей)
arp -d ip_address - удаляет нужный адрес из таблицы
arp -d * - удаление всей таблицы

linux:
arp -e - показать текущую таблицу arp (можно еще -v для подробностей)
arp -d ip_address - удаляет нужный адрес из таблицы
ip -s -s neigh flush all - удаление всей таблицы (т.к. arp -d * не работает)

```
8*. Установите эмулятор EVE-ng.  
Инструкция по установке - https://github.com/svmyasnikov/eve-ng  
Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng.
```
```