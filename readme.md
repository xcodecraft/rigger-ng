# rigger-ng

## 状态

0.1.0  alpha

### 主要目标:
#### 对项目(系统) 进行运行管理
#### 对项目(系统) 进行开发管理

```
程序  =  数据结构 + 算法
系统  =  程序     + 资源
```

演示:
``` shell
./rgdemo conf  -s test -e dev
./rgdemo start -s test -e dev

./rgdemo info  -s test -e dev
./rgdemo check -s test -e dev
```

# [依赖](doc/depends.md)

#使用:

``` shell

 mkdir ~/devspace ; cd ~/devspace/
 git clone git@github.com:xcodecraft/rigger-ng.git
 source  ./rigger-ng/myrg.bashrc

 rg help
```

## [使用指南] (doc/use_guide.md)
## extends

### [res](src/extends/res/readme.md)
### [module](src/extends/moduls/readme.md)
