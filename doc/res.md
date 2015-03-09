#

## modul & using


通过 modul 和 using 为rg 提供了复用机制

### 示例
```
_mod:
    - !R.modul
        _name : "m1"
        _res  :
            - !R.vars
                test_case : "A"
            - !R.echo
                value : "${TEST_CASE}"
            - !R.assert_eq
                value : "${TEST_CASE}"
                expect : "A"
```
```
- !R.using
    path          : "${PRJ_ROOT}/_rg/modul.yaml"
    modul         : "m1"
```
