#extends/pylon

## pylon_web
* MOD_TAG
* MOD_ENTRY
* MOD_INCLUDE

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
