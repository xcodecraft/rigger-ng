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
RGENV=`basename "$1"`
cd $SHELL_DIR/etc
if test -e $RGENV   ; then 
    if test -L rg_env.py ; then 
        rm rg_env.py
    fi
    ln -s $RGENV   rg_env.py
    echo "rigger-ng setup success!"
else 
    echo $RGENV not exists;
fi
