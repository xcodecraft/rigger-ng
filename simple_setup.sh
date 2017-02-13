DST=/home/x/tools/rigger-ng
PKG=/home/x/tools/pkgs/rigger-ng-simple
rm -rf $DST
cp -r ./ $PKG
ln -s $PKG/src  $DST
cd $DST ;
./setup.sh centos_xcc.py
