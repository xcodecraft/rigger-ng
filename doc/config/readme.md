# 配置文件



配置文件是 RG的 DSL, 　它通过yaml 并约定成为　_rg/run.yaml ;

配置文件的结构为：

``` yaml
  _env:
      - !R.env
          _name: "dev"
      - !R.env
          _name: "test"
      - !R.env
          _name: "online"
  _sys:
      -  !R.system
          _name: "api"
      -  !R.system
          _name: "console"

```

多环境、多系统定义组成。

* [核心定义](core.md)
* [moduls](moduls.md)
* [vars](vars.md)
* [res](inner_res.md)

[示例](prj_run.md)