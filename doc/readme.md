# rigger-ng 
 在多运行环境下
* 对项目(系统) 进行运行管理
* 对项目(系统) 进行开发管理


** 为什么需要？**
如果说

> 程序  =  数据结构  + 算法
那么系统即是　程序 +资源。　系统在不同的环境下，依赖的外部资源是不同的。因此如何方便管理、配置不同环境的资源是在软件开发过程中是个麻烦的问题。而rigger 正是为了解决此问题而存在的。


## 安装

[检查依赖](depends.md)

####  下载源码

``` shell
 mkdir ~/devspace ; cd ~/devspace/
 git clone git@github.com:xcodecraft/rigger-ng.git
```
###　个人环境

```SHELL
#mac环境
./setup/mac.sh
#centos 
./setup/centos.sh　　
```
### 团队环境

* 使用团队发布工具部署到需析机器
* 执行 setup.sh <platform>.py

## 使用
*  [使用指南](use_guide.md)
*  [FAQ](faq.md)

# 扩展&开发
* [扩展module](moduls.md)
* [开发指南](dev_guide.md)
* [模板](template.md)

