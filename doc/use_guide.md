#使用指南

## 查看帮助
```
rg help
```


## 项目初始化

``` shell
cd <you-project>
rg init

```

## 编辑 [_rg/run.yaml](prj_conf.md)


## 运行控制
示例:
```
cd ~/devspace/rigger-ng/demo ;
rg conf -e dev -s web,test
rg start
rg stop
rg clean
```


##[项目配置示例](example.md)



### 编辑 run.yaml

### 指令
``` shell
cd <you-project>
    rg conf  -s test -e dev
    rg start
    rg stop
    rg restart
    rg reload
    rg clean
    rg help
    rg help res
```
