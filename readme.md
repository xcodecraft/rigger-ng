# rigger-ng

## 状态

0.7.0  beta

## 主要目标:
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

## 个人开发
``` shell

 mkdir ~/devspace ; cd ~/devspace/
 git clone git@github.com:xcodecraft/rigger-ng.git
 cd rigger-ng ;
 setup.sh rg_envs/<platform>.py
 source  ./rigger-ng/myrg.bashrc

 rg help
```
## 团队使用

### 配置[团队的平台环境](doc/rg_env.md)
### 部署
``` shell
//1 .使用团队发布工具部署到需析机器
//2. 执行 setup.sh rg_envs<platform>.py
```

## [使用指南] (doc/use_guide.md)
## extends

### [res](src/extends/res/readme.md)
### [module](src/extends/moduls/readme.md)
