1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.  

git show aefea
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545  
комментарий: Update CHANGELOG.md


2. Какому тегу соответствует коммит 85024d3?

git show 85024d3  
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)

4. Сколько родителей у коммита b8d720? Напишите их хеши.  

git show b8d720  
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5  
Merge: 56cd7859e 9ea88f22f

git show 56cd7859e  
commit 56cd7859e05c36c06b56d013b55a252d0bb7e158

git show 9ea88f22f  
commit 9ea88f22fc6269854151c571162c5bcf958bee2b

6. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.

git log --oneline v0.12.23..v0.12.24  
33ff1c03b (tag: v0.12.24) v0.12.24  
b14b74c49 [Website] vmc provider links  
3f235065b Update CHANGELOG.md  
6ae64e247 registry: Fix panic when server is unreachable  
5c619ca1b website: Remove links to the getting started guide's old location  
06275647e Update CHANGELOG.md  
d5f9411f5 command: Fix bug when using terraform login on Windows  
4b6d06cc5 Update CHANGELOG.md  
dd01a3507 Update CHANGELOG.md  
225466bc3 Cleanup after v0.12.23 release

7. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).

git log --oneline -S 'func providerSource'  
5af1e6234 main: Honor explicit provider_installation CLI config when present  
8c928e835 main: Consult local directories as potential mirrors of providers

первое упоминание в коммите commit 8c928e83589d90a031f811fae52a81be7153e82f


8. Найдите все коммиты в которых была изменена функция globalPluginDirs.

находим файл с определением данной функции  

git grep -p "globalPluginDirs"  
commands.go=func initCommands(  
commands.go:            GlobalPluginDirs: globalPluginDirs(),  
commands.go=func credentialsSource(config *cliconfig.Config) (auth.CredentialsSource, error) {  
commands.go:    helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())  
internal/command/cliconfig/config_unix.go=func homeDir() (string, error) {  
internal/command/cliconfig/config_unix.go:              // FIXME: homeDir gets called from globalPluginDirs during init, before  
plugins.go=import (  
plugins.go:// globalPluginDirs returns directories that should be searched for  
plugins.go:func globalPluginDirs() []string {

определяем, что файл называется plugin.go, ищем коммиты, которые меняли данную функцию в этом файле  
(в опциях указан флаг --no-patch, чтобы убрать вывод кода самого изменения)

git log -L :globalPluginDirs:plugins.go --no-patch --pretty=format:'%H'  
78b12205587fe839f10d946ea3fdc06719decb05  
52dbf94834cb970b510f2fba853a5b49ad9b1a46  
41ab0aef7a0fe030e84018973a64135b11abcd70  
66ebff90cdfaa6938f26f908c7ebad8d547fea17  
8364383c359a6b738a436d1b7745ccdce178df47


9. Кто автор функции synchronizedWriters?  

git log --oneline -S'func synchronizedWriters' --pretty=format:'%h %an %ae'  
bdfea50cc James Bardin j.bardin@gmail.com  
5ac311e2a Martin Atkins mart@degeneration.co.uk  
отсюда автор Martin Atkins mart@degeneration.co.uk

