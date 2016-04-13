# 扩展的资源

**扩展资源与平台有关**

## pylon


``` yaml
_sys:
    -  !R.system
        _name: "pylon_autoload"
        _res:
            - !R.pylon_autoload
                include: "${PRJ_ROOT}"

    -  !R.system
        _name: "pylon_router"
        _res:
            - !R.pylon_router
                include: "${PRJ_ROOT}/test/data/"

```

#### pylon_autoload

#### pylon_router


## websys

#### fpm(fpm_base):

#### nginx_conf(nginx_conf_base):

#### mysql(mysql_base):


#### daemon:

#### daemon_php:

#### beanstalkd :

#### varnishd  :

#### crontab  :
