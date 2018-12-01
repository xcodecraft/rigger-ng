#内建RES


## vars

``` yaml
    !R.vars:
        A: 1
        B: "hello"
```
## echo

``` yaml
        !R.echo :
            value : "${PRJ_ROOT}"
```

## assert_eq
``` yaml

    !R.assert_eq
        value  : "${APP_SYS}"
        expect : "test"

```

