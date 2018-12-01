DST=${HOME}/rigger-ng
PKG=${HOME}/devspace/rigger-ng/src

unlink $DST
ln -s $PKG $DST
cd $DST ;
./setup.sh centos_xcc.py
