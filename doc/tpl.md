# 交互式的模板引擎

## 示例

###交互过程
```
what's you name? default(boy) exit(q)
zwj
love rg ? [LOVE] ? (y/n) default(y) exit(q)
y
```
结果
```
echo "this is rg tpl"
echo "Hi,zwj"
echo "love rg?"
echo "you love too! "
```


###交互过程
```
what's you name? default(boy) exit(q)
dog
love rg ? [LOVE] ? (y/n) default(y) exit(q)
n
```

结果
```
echo "this is rg tpl"
echo "Hi,dog"
echo "love rg?"
```



#### file
``` bash
echo "this is rg tpl"
echo "Hi,%{YOUNAME}"
echo "love rg?"
#% T.LOVE : {
echo "you love too! "
#% }
#% T.DB == "mysql" : {
echo "mysql is free! "
#% }
#% T.DB == "orcal" : {
echo "you are tuhao!"
#% }
```

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
