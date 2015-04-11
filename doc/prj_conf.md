# prj.yaml

## 示例
``` yaml
  _env:
      - !R.env
          _name: "dev"
          _res:
            - !R.vars
                prj_root : "${HOME}/devspace/rigger-ng/demo"
            - !R.path
                dst: "${PRJ_ROOT}/run,${PRJ_ROOT}/run/demo"


  _sys:
      -  !R.system
          _name: "test"
          _res:
              - !R.vars
                      TEST_CASE: "${PRJ_ROOT}/test/main.py"
              - !R.echo
                  value : "${TEST_CASE}"
              - !R.file_tpl
                  tpl: "${PRJ_ROOT}/files/prj_tpl.yaml"
                  dst: "${PRJ_ROOT}/files/prj_use.yaml"
```
## 规则
包括：
* _env  : 可包括多个 !R.env 对象。
* _sys :  可包括多个 !R.system 对象

资源运行结构:

  系统 X 在 A 环境运行:
  ```
  rg start -s X -e A
  env: A    -> system: X
  ```

  系统 X 在 A+debug 环境运行:
  ```
  rg start -s X -e A,debug
  env: A  -> env:debug  -> system: X
  ```

## 约定
_name  名称
_res   资源

*rg 所依赖的属性，都以'_'开头*
