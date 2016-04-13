# 扩展的资源

**扩展资源与平台有关**

## pylon

## websys

``` yaml
_sys:
    -  !R.system
        _name: "pylon_autoload"
        _res:
            - !R.pylon_autoload
                include: "${PRJ_ROOT}"

    -  !R.system
        _name: "pylon_router"
        _res:
            - !R.pylon_router
                include: "${PRJ_ROOT}/test/data/"

```

#### pylon_autoload

#### pylon_router
