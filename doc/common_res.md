#常用资源

## daemon

``` yaml

-  !R.system
    _name : "daemon"
    _res  :
        - !R.vars
            PHP_INI   : "${PRJ_ROOT}/conf/used/web_fpm.ini"
            PHP_BIN   : "/usr/local/php/bin/php"
        - !R.daemon
            script   : "${PRJ_ROOT}/src/daemon.sh"
            tag      : "sh"
        - !R.daemon_php
            script   : "${PRJ_ROOT}/src/daemon.php"
            tag      : "php"
```



