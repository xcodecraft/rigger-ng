#!/bin/bash
echo "****************This is Shell Test Scrite***********"
echo ${PRJ_ROOT}

case $1 in
    _config)
        exit;
        ;;
    _data)
        exit;
        ;;
    _start)
        echo "${X}-${Y}"
        exit;
        ;;
    _stop)
        echo " Exec stop "
        exit;
        ;;
esac

echo "*****************End***********"

