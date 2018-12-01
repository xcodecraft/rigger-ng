abs_path() { odir=`pwd`; cd `dirname $1`; pwd; cd "${odir}"; }
MYDIR=`abs_path "$0"`
cd $MYDIR

rg  conf -e dev -s test
rg  start 
rg  info
