#RG_ENV

RG所支持的资源管理依赖于　rgenv 所设置值。它安装在 /etc/rigger-ng/rg_env.py

###  支持自己系统环境。

你可以修改 /etc/rigger-ng/rg_env.py 来配置你所需要的环境 ;

例如：
```pyhton 

  from setting import rgenv
  def rgenv_enable() :
      rgenv['PHP_BIN']    = "/usr/local/php-5.6/bin/php"
      rgenv['PHP_FPM']    = "/usr/local/php-5.6/sbin/php-fpm"
      rgenv['PHP_INI']    = "/usr/local/php-5.6/lib/php.ini"
      rgenv['VARNISHD']   = "/usr/local/varnish-4.1.2/sbin/varnishd"
      rgenv['VARNISHADM'] = "/usr/local/varnish-4.1.2/bin/varnishadm"
      rgenv['RG_DEVPATH'] = "/data/${USER}/devspace/rigger-ng"
      rgenv['ZDAEMON']    = "/usr/local/python/bin/zdaemon"
      rgenv['BEANSTALKD'] = "/usr/local/beanstalkd/bin/beanstalkd"
      rgenv['NGINX_CONF'] = "/usr/local/nginx/conf/include/"
```