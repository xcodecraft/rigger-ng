# 熟记指令
## help 
```
rg help [<command> [<subcommand>]] 
eg:
rg help res
rg help res mysql
```

# 系统控制指令
## conf

```
rg conf -e <env> -s <sys>
```
## start,stop,restart,reload

```
rg start [-s <sys>]
rg stop  [-s <sys>]
rg restart [-s <sys>]
rg reload [-s <sys>]
```

# 工程指令
## rc 
## sonar

# 其它指令
## init
```
rg init 
```

## tpl 


```
rg tpl -t <tpl path> -o <dest path>
```

可以通过tpl指令, 生成新工程

