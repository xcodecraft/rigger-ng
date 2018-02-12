PID_FILE=$1
CMD=$2
if test -z $PID_FILE  ;then
  exit 0 ;
fi
if test -z $CMD ;then
  exit 0 ;
fi

if test -e $PID_FILE ;
then
  PID=`cat $PID_FILE`
  PORC_EXIST=`ps --no-heading $PID | wc -l`

  if test $PORC_EXIST = "1" ;
  then
    kill -$CMD $PID
  else
  echo "process not exists pid:$PID"
  fi

else
  echo "$PID_FILE not exists "
fi
exit 0 ;
