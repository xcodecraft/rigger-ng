#RG_ENV

*rg_env.py 是rigger-ng 依赖各系统服务的路径设置文件*

## 如何支持自己系统环境。

根据 [rgenv_tpl.py](../src/rg_envs/rgenv_tpl.py) 编写你的 you_plat.py

例如： centos_ayb.py
```pyhton

  from setting import rgenv
  def rgenv_enable() :
      rgenv['PHP_BIN']    = "/usr/local/php-5.6/bin/php"
      rgenv['PHP_FPM']    = "/usr/local/php-5.6/sbin/php-fpm"
      rgenv['PHP_INI']    = "/usr/local/php-5.6/lib/php.ini"
      rgenv['VARNISHD']   = "/usr/local/varnish/sbin/varnishd"
      rgenv['VARNISHADM'] = "/usr/local/varnish/bin/varnishadm"
      rgenv['RG_DEVPATH'] = "/data/${USER}/devspace/rigger-ng"
      rgenv['ZDAEMON']    = "/usr/local/python/bin/zdaemon"
      rgenv['BEANSTALKD'] = "/usr/local/beanstalkd/bin/beanstalkd"
      rgenv['NGINX_CONF'] = "/usr/local/nginx/conf/include/"
```

生效配置
```
    setup.sh  ./etc/<your>.py
```
