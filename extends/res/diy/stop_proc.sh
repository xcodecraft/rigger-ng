PID_FILE=$1
NAME=$2
if ! test -e $PID_FILE;then
    echo "$PID_FILE not exists, cant not  stop!"
    exit 0 
fi

if ! test -s $PID_FILE;then
    echo "$PID_FILE is empty , cant not  stop!"
    rm $PID_FILE ;
    exit 0 
fi
echo "$NAME  $PID_FILE will stop";
while true; do
        echo ".";
        cat $PID_FILE | xargs kill   ;
        RC=$?
        if ! test $RC -eq 0 ;  then 
            sleep 1
            echo "kill return code is  $RC"
            continue 
        else
            sleep 1
            if  test -e $PID_FILE;then
                rm $PID_FILE   
            fi
            echo "$NAME have stoped " 
            exit 0 
        fi
done

