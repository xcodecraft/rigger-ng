# rigger-ng 0.7.0  beta

## 主要目标:
#### 对项目(系统) 进行运行管理
#### 对项目(系统) 进行开发管理

```
程序  =  数据结构 + 算法
系统  =  程序     + 资源
```
## 理解思想 [PPT](https://github.com/xcodecraft/rigger-ng/blob/doc/ppt/rigger2.pdf)




## 使用

####  下载源码
``` shell
 mkdir ~/devspace ; cd ~/devspace/
 git clone git@github.com:xcodecraft/rigger-ng.git
```
#### 配置[平台环境](doc/rg_env.md)

#### 设定alias 方便使用
```
RG_ROOT=$HOME/devspace/rigger-ng/src
alias rg='$RG_ROOT/rg'
alias srg='sudo $RG_ROOT/rg''
```





### 团队使用

### 部署
``` shell
//1 .使用团队发布工具部署到需析机器
//2. 执行 setup.sh ./etc/<platform>.py
```

## [使用指南] (doc/use_guide.md)
### [内建res](doc/res.md)
### [扩展res](src/extends/res/readme.md)
### [扩展module](src/extends/moduls/readme.md)

## [开发指南] (doc/dev_guide.md)
