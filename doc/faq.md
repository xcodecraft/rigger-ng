### 为什么要开发rigger-ng ?

项目的自动化维护是一个很大的痛点, 需要对系统的资源进行管理。 特别在多人开发，多环境支持上！

### 查看运行中的问题

加上调整参数 -d 1
```
    rg start -d 1
```
### 为什么用yaml ?
 ** yaml 的优点: **
- yaml 的可读性好。 
- yaml和脚本语言的交互性好。
- yaml使用实现语言的数据类型。 
- yaml有一个一致的信息模型。 
- yaml易于实现。

** 其它格式的不足 **
- ini 只能表达两层结构,表达受限 
- json 可读性差点
- xml 繁琐

### 如何防止demo,online环境下，执行初始化系统？

``` yaml
      - !R.system
          _name   : "init"
          _limit :
              "envs"   : "demo,online"
              "passwd" : "xyz"
          _res    :
              - !R.echo
                  value         : "limit is pass!"
```

设置 system的 _limit属性
* envs   受限的环境
* passwd  受限下还可执行的可令

``` shell
rg start -e dev -s init    //run  init system 
rg start -e online -s init  //ignore init system 
rg start -e online -s init -p xyz  //run init system 
```
