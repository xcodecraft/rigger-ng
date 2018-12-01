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

##crontab 

管理 crontab 
``` yaml
  _sys:
      -  !R.system
          _name: "mysys"
          _res:
              - !R.echo
                  value : "hello"
              - !R.crontab
                  sudo: True
                  cron: "${PRJ_ROOT}/src/exampl.cron"
```

``` yaml
  _sys:
      -  !R.system
          _name: "mysys"
          _res:
              - !R.crontab
                  sudo: True
                  key : "A"
                  cron: "${PRJ_ROOT}/src/exampl1.cron"
               - !R.crontab
                  sudo: True
                  key : "B"
                  cron: "${PRJ_ROOT}/src/exampl2.cron"
```
