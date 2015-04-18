#! /bin/bash
if [ $# -lt 7 ] 
then
    echo "Usage: $0 -b /usr/local/php-5.3/sbin/php-fpm -c /usr/local/php-5.3/etc/php-fpm-9001.conf -f /usr/local/php-5.3/etc/php.ini -p /path/to/prefix -r /home/q/system/wan -d {start|stop|restart|reload} -n /path/to/rigger/run"
    exit
fi
while getopts "b:c:f:p:r:n:d:" OPTION
do
    case $OPTION
        in
        b) bin=$OPTARG;; # php-fpm
        c) conf=$OPTARG;; # php-fpm.conf
        f) phpini=$OPTARG;; # php.ini
        p) prefix=$OPTARG;; # prefix
        r) prjroot=$OPTARG;; #prjroot
        n) runpath=$OPTARG;; #rigger runpath
        d) do=$OPTARG;; # start,stop,reload
    esac
done

php_fpm_BIN=${bin}
php_fpm_CONF=${conf}
php_fpm_PREFIX=$runpath/${prefix}
php_fpm_PID=$php_fpm_PREFIX/fpm.pid
php_fpm_PHPINI=${phpini}

php_opts="--fpm-config $php_fpm_CONF -c $php_fpm_PHPINI"

#如果没有自定义fpm_conf路径，则使用自动生成pid和prefix路径
[ -n "$prefix" ] && php_opts="$php_opts --pid $php_fpm_PID --prefix $php_fpm_PREFIX"

wait_for_pid () {
    try=0

    while test $try -lt 35 ; do

        case "$1" in
            'created')
            if [ -f "$2" ] ; then
                try=''
                break
            fi
            ;;

            'removed')
            if [ ! -f "$2" ] ; then
                try=''
                break
            fi
            ;;
        esac

        echo -n .
        try=`expr $try + 1`
        sleep 1

    done

}

#检查fpm_conf文件是否正确生成，否则报错
#如果是自定义conf，也应该正确存在
check_fpm_conf () {
   if [ ! -f $php_fpm_CONF ]; then
       echo '[ERROR] fpm_conf_file' $php_fpm_CONF 'is not exsit!'
       exit 1
   fi
}

force-quit () {
   echo 'force terminating php-fpm : '
   ps auxw | grep -v fpm_ctrl.sh | grep -v grep | grep ${prefix} 
   pidcount=`ps auxw | grep -v fpm_ctrl.sh | grep -v grep | grep ${prefix} | wc -l `
   pids=`ps auxw | grep -v fpm_ctrl.sh | grep -v grep | grep ${prefix} | awk '{print $2}'`
   [ $pidcount = "0" ] && echo nothing to kill || kill -9 $pids;
   echo -n 'cleaning fpm-conf : '
   [ "$prefix" -a -d $php_fpm_PREFIX ] && rm -rf $php_fpm_PID
   echo ' done.'
}

case "$do" in
    config)
        echo -n "Configuring php-fpm "
        #把环境变量link至/var/run/$prefix
        [ -e $php_fpm_PREFIX/env.conf ] && rm -f $php_fpm_PREFIX/env.conf
        ln -s $prjroot/run/${prefix}.env $php_fpm_PREFIX/env.conf
        echo done
        ;;
    start)
        echo -n "Starting php-fpm "
   
        #检查FPM配置是否生成 
        check_fpm_conf

        #如果有pid文件且进程存在，结束
        if [ -r $php_fpm_PID ]; then
            pid=`cat $php_fpm_PID`
            proc=`ps --no-heading $pid | wc -l`
            [ $proc = "1" ] && echo "php-fpm already started with PID: $pid " && exit 0
        fi
        #忽略有pid进程不存在的情况

        $php_fpm_BIN $php_opts

        if [ "$?" != 0 ] ; then
            echo " failed"
            exit 1
        fi

        wait_for_pid created $php_fpm_PID

        if [ -n "$try" ] ; then
            echo " failed"
            exit 1
        else
            echo " done"
        fi
    ;;

    stop)
        echo -n "Gracefully shutting down php-fpm "
       
        #如果没有pid，强行清理
        if [ ! -r $php_fpm_PID ] ; then
            echo "warning, no pid file found - php-fpm is not running ?"
            force-quit
            exit 0
        fi

        #如果有pid文件且进程存在，使用Kill方法
        #有pid文件但进程不存在，干掉pid文件
        if [ -r $php_fpm_PID ]; then
            pid=`cat $php_fpm_PID`
            proc=`ps --no-heading $pid | wc -l`
            [ $proc = "0" ] && rm -rf $php_fpm_PID && echo " cleaned" && exit 0
        fi
        
        kill -QUIT $pid 
        
        wait_for_pid removed $php_fpm_PID

        if [ -n "$try" ] ; then
            echo " failed. Use force-quit"
            force-quit
        else
            echo " done"
        fi
    ;;

    restart)
        $0 stop
        $0 start
    ;;

    reload)

        echo "Reload service php-fpm "

        if [ ! -r $php_fpm_PID ] ; then
            echo "warning, no pid file found - php-fpm is not running ?"
            exit 0
        fi

        kill -USR2 `cat $php_fpm_PID`

        echo " done"
    ;;

    clean)

        echo -n "Cleaning fpm conf in $php_fpm_PREFIX ..."
        [ "$prefix" -a -d $php_fpm_PREFIX ] && rm -rf $php_fpm_PREFIX
        echo " done."
    ;;

    *)
        echo "Usage: $0 {config|start|stop|force-quit|restart|reload|clean}"
        exit 1
    ;;

esac
