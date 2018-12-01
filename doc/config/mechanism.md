
#include

## 示例
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
                    - "/data/x/tools/env_setting/env/ayb.yaml"
                    - "/data/x/framework/pylon-ng/rigger/pylon.yaml"
```

include 用于引入公共的配置信息

#module