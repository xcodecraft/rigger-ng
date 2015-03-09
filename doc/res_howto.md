# 如何组织资源


通过 ${RES_BIN_BASE} 的变量来隔离不同操作系统变化 

```
!R.mysql :
  bin : "${RES_BIN_BASE}/bin/mysql"

!R.varnish
  bin : "${RES_BIN_BASE}/sbin/varnishd"
  
```
