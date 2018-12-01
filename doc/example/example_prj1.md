
``` yaml
  _env:
      - !R.env
          _name : "_local_deploy"
          _res  :
              - !R.project
                  root        : "${HOME}/devspace/plato"
                  name        : "plato"
              - !R.vars
                  PHP_ERROR    : "E_ALL & ~E_NOTICE"
                  FPM_USER     : "${USER}"
                  RUN_USER     : "${USER}"
                  SDK_PATH     : "${HOME}/devspace/platform_sdks/src/plato"
                  PLATFORM_SDK : "${HOME}/devspace/platform_sdks/src/"
      - !R.env
          _name : "_safe_deploy"
          _res  :
              - !R.project
                  root      : "/data/x/projects/plato"
                  name      : "plato"
              - !R.vars
                  PHP_ERROR    : "E_ALL & ~E_NOTICE"
                  FPM_USER     : "ayb"
                  RUN_USER     : "ayb"
                  SDK_PATH     : "/data/x/sdks/platform_sdks/plato"
                  PLATFORM_SDK : "/data/x/sdks/platform_sdks/"


      - !R.env
          _name    : "_speed_max"
          _res :
              - !R.vars
                  MAX_CHILDREN      : "20"
                  START_SERVERS     : "5"
                  MIN_SPARE_SERVERS : "5"
                  MAX_SPARE_SERVERS : "10"
                  
     - !R.env
          _name    : "_speed_min"
          _res :
              - !R.vars
                  MAX_CHILDREN      : "5"
                  START_SERVERS     : "2"
                  MIN_SPARE_SERVERS : "1"
                  MAX_SPARE_SERVERS : "3"



      - !R.env
          _name    : "debug"
          _res :
              - !R.vars
                  PHP_ERROR : "E_ALL & ~E_NOTICE"
                  DEBUG     : "ON"
                  LOG_MODE  : "DEBUG"

      - !R.env
          _name    : "release"
          _res :
              - !R.vars
                  PHP_ERROR : "E_ERROR"
                  DEBUG     : "XOFF"
                  LOG_MODE  : "ONLINE"
                  
                  
     - !R.env
          _name    : "_dev"
          _res :
              - !R.vars
                  BASE_DOMAIN : "plato.${USER}.dev.xcodecraft.com"
                  CONFSVC_URL : "api.${BASE_DOMAIN}"
                  REDIS_SPACE : "${USER}"

                  DB_HOST    : "xxx.xxx.xxx"
                  DB_NAME    : "plato_${USER}"
                  DB_USER    : "xxx"
                  DB_PWD     : "xxx"
                  ADMIN_PORT : "80"
                  ALLOW_IP   : "allow all ; "


      - !R.env
          _name    : "_demo"
          _res :
              - !R.vars
                  BASE_DOMAIN : "plato.demo.xcodecraft.com"
                  CONFSVC_URL : "api.${BASE_DOMAIN}"

                  REDIS_SPACE : "demo"

                  DB_HOST     : "xxx.xxx"
                  DB_NAME     : "plato_demo"
                  DB_USER     : "xxx"
                  DB_PWD      : "xxx"
                  ADMIN_PORT : "80"
                  ALLOW_IP   : "allow all ; "


      - !R.env
          _name    : "base"
          _res :
              - !R.vars
                  PRJ_NAME        : "plato"
                  PRJ_KEY         : "plato"
                  HTTP_PORT       : "8086"
                  SRC_ROOT        : "${PRJ_ROOT}/src"
                  PYLON           : "/data/x/framework/pylon-ng"
                  BASE_INCLUDE    : "${PRJ_ROOT}/src/logic:${SDK_PATH}"

                  WORK_SPACE      : "/data/${RUN_USER}/plato/work_space/"
                  TEMP_SPACE      : "/data/${RUN_USER}/plato/temp_space/"
                  STORE_GIT       : "/data/${RUN_USER}/plato/store_git/"
                  PUB_SPACE       : "/data/${RUN_USER}/plato/pub_space/"
                  GIT_PATH        : "/usr/local/bin/git"

              - !R.path
                  dst  : "${PRJ_ROOT}/conf/used/,${PRJ_ROOT}/tmp"
              - !R.path
                  dst  : "${STORE_GIT},${WORK_SPACE},${PUB_SPACE},${TEMP_SPACE},/data/xhprof/${PRJ_KEY}"
                  sudo : True
                  keep : True

      - !R.env
          _name    : "dev"
          _mix     : "_local_deploy,_dev,base,_speed_min,debug"
      - !R.env
          _name    : "lab"
          _mix     : "_safe_deploy,_lab,base,_speed_min,debug"
      - !R.env
          _name    : "demo"
          _mix     : "_safe_deploy,_demo,base,_speed_min,debug"

          
          
 _sys:
      - !R.system
          _name : "init"
          _res  :
              - !R.vars
                  MODULES : ".:${PRJ_ROOT}/src/init/:${PRJ_ROOT}/src/logic:${SDK_PATH}"
                  PHP_INI : "${PRJ_ROOT}/conf/used/init_php.ini"
                  PHP_BIN : "/usr/local/php-5.6/bin/php"
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
                  ini    : "${PHP_INI}"
                  bin    : "/usr/local/php-5.6/bin/php"
                  script : "${PRJ_ROOT}/src/init/sys_init.php"
              - !R.shell
                  script : "${PRJ_ROOT}/src/init/env_init.sh"

      # 管理后台
      -  !R.system
              _name : "admin"
              _res  :
                  - !R.vars
                      APP_SYS    : "admin"
                      DOMAIN     : "admin.${BASE_DOMAIN}"
                      SOCK_FILE  : "${RUN_PATH}/fpm.sock"

                  - !R.using
                      path  : "/data/x/tools/rigger-ng/extends/moduls/pylon.yaml"
                      modul : "pylon_web"
                      args  : !R.vars
                          MOD_TAG     : "admin"
                          MOD_ENTRY   : "${PRJ_ROOT}/src/apps/admin"
                          MOD_INCLUDE : "${PRJ_ROOT}/src/apps/admin:${BASE_INCLUDE}:${PRJ_ROOT}/src/web_inf"
                          
                          
      #读服务
      -  !R.system
              _name : "api"
              _res:
                  - !R.vars
                      SOCK_FILE : "${RUN_PATH}/fpm.sock"
                      DOMAIN    : "api.${BASE_DOMAIN}"
                      CONF      : "${PRJ_ROOT}/conf"
                      API_PORT  : "8086"
                      MODULES   : "${PRJ_ROOT}/src/logic:${PRJ_ROOT}/src/apps/api:${PRJ_ROOT}/conf/:${SDK_PATH}"

                  - !R.using
                      path  : "/data/x/tools/rigger-ng/extends/moduls/pylon.yaml"
                      modul : "pylon_web"
                      args  : !R.vars
                              MOD_INCLUDE     : "${MODULES}:${SDK_PATH}"
                              MOD_ENTRY       : "${PRJ_ROOT}/src/apps/api"
                              MOD_TAG         : "api"

                  - !R.cmd
                      cmd : "/usr/bin/curl -H \"host:${DOMAIN}\" \"127.0.0.1:${HTTP_PORT}/monitor\" -X GET ; echo \"\" "

                  
```

