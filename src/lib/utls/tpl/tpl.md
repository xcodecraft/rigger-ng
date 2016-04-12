# TPL 使用

``` python

        utls.tpl.var.clean()
        utls.tpl.var.import_str("need_admin=TRUE,mode=rest")
        ngx    = utls.tpl.engine()
        path   = ngx.proc_path("/home/#%T.need_admin:TRUE/abc")
```


