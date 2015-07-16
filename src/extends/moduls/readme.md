#extends/pylon

## pylon_web
* MOD_TAG    TAG
* MOD_ENTRY  入口，router入口目录
* MOD_INCLUDE  需要的PHP include
* php: /usr/local/php-5.6

示例
```
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

```
            - !R.using
                path  : "/home/x/tools/rigger-ng/extends/moduls/pylon.yaml"
                modul : "pylon_php"
                args  : !R.vars
                    MOD_TAG : "test"
                    MOD_INCLUDE: "${PRJ_ROOT}/test:${PRJ_ROOT}/src"
```
