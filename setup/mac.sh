DST=${HOME}/rigger-ng
PKG=${HOME}/devspace/rigger-ng/src

unlink $DST
ln -s $PKG $DST
cd $DST ;
./setup.sh mac.py
cd /usr/local/bin
sudo unlink rg
sudo ln -s ${DST}/rg rg


echo "Welcome use Rigger-NG! "
echo "eg: rg help"
