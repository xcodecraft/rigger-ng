#!/bin/bash
echo "****************************************************"
echo "****************This is Demo Shell Scrite***********"
echo ${PRJ_ROOT}

case $1 in
    _config)
        echo " Exec Config "
        exit;
        ;;
    _data)
        echo " Exec Data "
        exit;
        ;;
    _start)
        echo " Exec start "
        exit;
        ;;
    _stop)
        echo " Exec stop "
        exit;
        ;;
esac

echo "*****************End***********"

