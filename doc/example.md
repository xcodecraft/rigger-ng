

## 初始化系统
``` yaml
      - !R.system
          _name : "init"
          _res  :
              - !R.vars
                  MODULES   : ".:${PRJ_ROOT}/src/init/:${PRJ_ROOT}/src/logic:${SDK_PATH}"
              - !R.mysql
                  host     : "${DB_HOST}"
                  name     : "${DB_NAME}"
                  user     : "${DB_USER}"
                  password : "${DB_PWD}"
                  sql      : "${PRJ_ROOT}/src/init/create_db.sql"

              - !R.using
                  path  : "/data/x/tools/rigger-ng/extends/moduls/pylon.yaml"
                  modul : "pylon_php"
                  args  : !R.vars
                      MOD_TAG     : "init"
                      MOD_INCLUDE : "./:${PRJ_ROOT}/src/init:${BASE_INCLUDE}"
              - !R.php
                  ini    : "${PRJ_ROOT}/conf/used/init_php.ini"
                  bin    : "/usr/local/php-5.6/bin/php"
                  script : "${PRJ_ROOT}/src/init/sys_init.php"
              - !R.shell
                  script : "${PRJ_ROOT}/src/init/env_init.sh"
```
