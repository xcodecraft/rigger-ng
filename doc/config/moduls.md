#modul机制

## 调用  !R.using

示例
``` yaml
- !R.using
    path  : "/home/x/tools/rigger-ng/extends/moduls/pylon.yaml"
    modul : "pylon_web"
    args  : !R.vars
        MOD_TAG     : "api_hero"
        MOD_ENTRY   : "${PRJ_ROOT}/src/api_hero"
        MOD_INCLUDE : "${PRJ_ROOT}/src/api_hero:${BASE_INCLUDE}"
```
- path  
- modul
- args

## 编写 !R.modul
示例
``` yaml
      - !R.modul
          _name : "pylon_web"
          _args :
              MOD_TAG:     None
              MOD_ENTRY:   None
              MOD_INCLUDE: None
          _res  :
              - !R.vars
                  tpl_root : "${PRJ_ROOT}/conf/options/"
                  use_root : "${PRJ_ROOT}/conf/used/"
              - !R.pylon_autoload
                  include  : "${MOD_INCLUDE}"
              - !R.pylon_router
                  include  : "${MOD_ENTRY}"
              - !R.nginx_conf
                  sudo     : true
                  src      : "${USE_ROOT}/${MOD_TAG}_ngx.conf"
                  tpl      : "${TPL_ROOT}/${MOD_TAG}_ngx.conf"
              - !R.fpm
                  sudo     : True
                  ini_tpl  : "${TPL_ROOT}/${MOD_TAG}_php.ini"
                  conf_tpl : "${TPL_ROOT}/${MOD_TAG}_fpm.conf"
```

- _name : 模块名称
- _args : 模块参数
- _res  : 模块资源

#pylon 扩展modul



## pylon_web
* MOD_TAG    TAG
* MOD_ENTRY  入口，router入口目录
* MOD_INCLUDE  需要的PHP include
* php: /usr/local/php-5.6

示例
``` yaml
- !R.using
    path  : "/home/x/tools/rigger-ng/extends/moduls/pylon.yaml"
    modul : "pylon_web"
    args  : !R.vars
        MOD_TAG     : "api_hero"
        MOD_ENTRY   : "${PRJ_ROOT}/src/api_hero"
        MOD_INCLUDE : "${PRJ_ROOT}/src/api_hero:${BASE_INCLUDE}"
```
## pylon_php
* MOD_TAG    TAG
* MOD_INCLUDE  需要的PHP include

``` yaml
- !R.using
    path  : "/home/x/tools/rigger-ng/extends/moduls/pylon.yaml"
    modul : "pylon_php"
    args  : !R.vars
        MOD_TAG : "test"
        MOD_INCLUDE: "${PRJ_ROOT}/test:${PRJ_ROOT}/src"
```
## phpunit

``` yaml
      -  !R.system
              _name : "test"
              _res:
                  - !R.vars
                      MODULES      : "${PRJ_ROOT}/src/logic:${PRJ_ROOT}/test/:${PRJ_ROOT}/conf/:${SDK_PATH}"

                  - !R.using
                      path  : "/data/x/tools/rigger-ng/extends/moduls/pylon.yaml"
                      modul : "phpunit"
                      args  : !R.vars
                          TEST_INCLUDE: "${MODULES}"
```

