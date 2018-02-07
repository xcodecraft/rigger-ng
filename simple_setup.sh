DST=/data/x/tools/rigger-ng
PKG=/data/x/tools/pkgs/rigger-ng-simple
rm -rf $DST
mkdir -p /data/x/tools/pkgs
cp -r ./ $PKG
ln -s $PKG/src  $DST
cd $DST ;
./setup.sh centos_xcc.py
