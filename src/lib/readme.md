# rigger-ng
## interface
rg 的关键抽象，用于扩展更多RES

### resouce
``` python
class resource (rg_conf.base):
    def _allow(self,context):
        pass
    def _before(self,context):
        pass
    def _after(self,context):
        pass
    def _start(self,context):
        pass
    def _stop(self,context):
        pass
    def _reload(self,context):
        pass
    def _config(self,context):
        pass

    def _data(self,context):
        pass
    def _check(self,context):
        pass
    def _clean(self,context):
        pass

```
### 项目资源结构

``` yaml

__env:
    - !R.vars
        name: "dev"

__prj: !R.project
       name: "rigger-ng"
       key:  "rg-ng"
       res:
        - !R.vars
                PRJ_NAME: "rg"
                PRJ_KEY : "RG_UT"


__sys:
    -  !R.system
        name: "test"
        res:
            - !R.vars
                    TEST_CASE: "${HOME}/devspace/rigger-ng/test/main.py"
            - !R.echo
                value : "${TEST_CASE}"
```


## utls
有用的工具模块
## res
## impl




