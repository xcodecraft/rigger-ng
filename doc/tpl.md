# 交互式的模板引擎

## 示例

###交互
```
what's you name? default(boy) exit(q)
zwj
love rg ? [LOVE] ? (y/n) default(y) exit(q)
y
chose db!
1: mysql
2: orcal
3 other DB
please chose DB exit( q )
1
```
###结果
```
echo "this is rg tpl"
echo "Hi,zwj"
echo "love rg?"
echo "love you too! "
echo "mysql is free! "
```


###交互
```
what's you name? default(boy) exit(q)
dog
love rg ? [LOVE] ? (y/n) default(y) exit(q)
n
chose db!
1: mysql
2: orcal
3 other DB
please chose DB exit( q             )
2
```

###结果
```
echo "this is rg tpl"
echo "Hi,dog"
echo "love rg?"
echo "you are tuhao!"
```



### 模板
``` bash
echo "this is rg tpl"
echo "Hi,%{YOUNAME}"
echo "love rg?"
#% T.LOVE : {
echo "love you too! "
#% }
#% T.DB == "mysql" : {
echo "mysql is free! "
#% }
#% T.DB == "orcal" : {
echo "you are tuhao!"
#% }
```

### yaml conf

``` yaml
YOUNAME: !T.input
    prompt : "what's you name?"
    default : "boy"

LOVE : !T.bool
    prompt : "love rg ?"
    default: "y"

DB : !T.chose
    prompt : "chose db!"
    options:
        - "mysql"
        - "orcal"
```

### 语法
```
%{VARNAME}

#% T.VARNAME : {

#% }
#% T.VARNAME =='value' : {

#% }
```
