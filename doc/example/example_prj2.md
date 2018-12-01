引用平台配置示例

``` yaml
_env:
    - !R.env
        _name : "define"
        _res  :
            - !R.vars
                PRJ_NAME : "plato"
                PRJ_KEY  : "plato"
            - !R.include
                    _path :
                    - "/data/x/tools/env_setting/env/xcodecraft.yaml"
                    - "/data/x/framework/pylon-ng/rigger/pylon.yaml"

    - !R.env
        _name    : "base"
        _res :
            - !R.vars
                HTTP_PORT    : "8086"
                SRC_ROOT     : "${PRJ_ROOT}/src"
                BASE_INCLUDE : "${PRJ_ROOT}/src/logic:${SDK_PATH}"
                WORK_SPACE   : "/data/${RUN_USER}/plato/work_space/"
                STORE_GIT    : "/data/${RUN_USER}/plato/store_git/"
                GIT_PATH     : "/usr/local/bin/git"
                SDK_PATH     : "/data/x/sdks/platform_sdks/plato"
                ADMIN_PORT : "80"
                ALLOW_IP   : "allow all ; "

            - !R.path
                dst  : "${PRJ_ROOT}/conf/used/,${PRJ_ROOT}/tmp"
            - !R.path
                dst  : "${STORE_GIT},${WORK_SPACE}"
                sudo : True
                keep : True

    - !R.env
        _name    : "dev"
        _mix     : "define,_local_deploy,base,_base,_dev,speed_min,debug"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.${USER}.dev.xcodecraft.cn"
                REDIS_SPACE : "${USER}"

    - !R.env
        _name    : "demo"
        _mix     : "define,_safe_deploy,_base,base,_demo,speed_min,debug"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.demo.xcodecraft.cn"
                REDIS_SPACE : "demo"


    - !R.env
        _name    : "test"
        _mix     : "define,_safe_deploy,_base,base,_test,speed_min,debug"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.test.xcodecraft.cn"
                REDIS_SPACE : "TEST"

    - !R.env
        _name    : "lab"
        _mix     : "define,_safe_deploy,_base,base,_lab,speed_min,debug"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.lab.xcodecraft.cn"
                REDIS_SPACE : "demo"

    - !R.env
        _name    : "ci"
        _mix     : "define,_ci_deploy,_base,base,_ci,speed_min,debug"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.ci.xcodecraft.cn"
                REDIS_SPACE : "demo"

    - !R.env
        _name    : "online"
        _mix     : "define,_safe_deploy,_base,base,_online,speed_max,release"
        _res :
            - !R.vars
                BASE_DOMAIN : "plato.xcodecraft.cn"
                CONFSVC_URL : "api.${BASE_DOMAIN}"
                REDIS_SPACE : "online"
                DB_HOST     : "xxxx.mysql.rds.aliyuncs.com"
                DB_NAME     : "plato_online"
                DB_USER     : "u_xxxx"
                DB_PWD      : "xxxx"
                ADMIN_PORT  : "80 "
                ALLOW_IP    : "allow 10.0.0.0/8;  allow 100.64.0.0/10 ;   deny all ; "


_sys:
    - !R.system
        _name  : "init"
        _limit :
            envs   : "demo,online"
            passwd : "plato"
        _res  :
            - !R.using
                modul : "ayb_init"
                args  : !R.vars
                    INCLUDE_PATH : "./:${PRJ_ROOT}/src/init:${BASE_INCLUDE}"
                    INIT_SQL     : "${PRJ_ROOT}/src/init/create_db.sql"
                    INIT_PHP     : "${PRJ_ROOT}/src/init/sys_init.php"
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
                    DOMAIN  : "api.${BASE_DOMAIN}"
                    PORT    : "8086"
                - !R.using
                    modul : "ayb_api"
                    args  : !R.vars
                            INCLUDE_PATH : "${PRJ_ROOT}/src/logic:${PRJ_ROOT}/src/apps/api:${PRJ_ROOT}/conf/:${SDK_PATH}"
                            API_ENTRY    : "${PRJ_ROOT}/src/apps/api"
                            TAG          : "api"



    -  !R.system
            _name : "tools"
            _res:
                - !R.using
                    modul : "ayb_php"
                    args  : !R.vars
                        TAG     : "tools"
                        INCLUDE_PATH : "./:${PRJ_ROOT}/src/init:${BASE_INCLUDE}"

    -  !R.system
            _name : "test"
            _res:
                - !R.using
                    modul : "ayb_unit"
                    args  : !R.vars
                        INCLUDE_PATH: "${PRJ_ROOT}/src/logic:${PRJ_ROOT}/test/:${PRJ_ROOT}/conf/:${SDK_PATH}"
                        API_ENTRY  : "${PRJ_ROOT}/src/apps/api"


```