from setting import rgenv

def rgenv_enable() :
    rgenv['PHP_BIN']    = "/usr/bin/php"
    rgenv['PHP_INI']    = "/etc/php5/cli/php.ini"
    rgenv['VARNISHD']   = "/usr/sbin/varnishd"
    rgenv['VARNISHADM'] = "/usr/bin/varnishadm"
    rgenv['RG_DEVPATH'] = "${HOME}/devspace/rigger-ng"

