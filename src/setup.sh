adirname() { odir=`pwd`; cd `dirname $1`; pwd; cd "${odir}"; }
SHELL_DIR=`adirname "$0"`

if test $# -ne 1 ; then
    echo $0  "<you_env.py>"
    exit 0
fi
if ! test -e "/usr/bin/python" ; then 
    echo "not found /usr/bin/python"
    echo "rigger-ng need python"
    exit 0
fi
ENV_TPL=`basename "$1"`
ETC_DIR="/etc/rigger-ng"
ETC_FILE="$ETC_DIR/rg_env.py"
cd $SHELL_DIR/etc_tpl
if test -f $ETC_FILE  ; then 
  echo "$ETC_FILE exists! "
else
  if test -e $ENV_TPL   ; then 
    sudo mkdir -p $ETC_DIR 
    sudo cp $ENV_TPL  $ETC_FILE 
    echo "rigger-ng setup success!"
  else 
      echo $ENV_TPL not exists;
      exit -1 ;
  fi

fi


if test -L /usr/local/bin/rg ; then 
  sudo rm /usr/local/bin/rg
fi
cd /usr/local/bin
sudo ln -s ${SHELL_DIR}/rg rg

echo ""
echo "---------------------------------------"
echo "Welcome use Rigger-NG! "
echo "eg: rg help"
echo "---------------------------------------"
