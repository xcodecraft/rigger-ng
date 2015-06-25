TAG=`cat src/version.txt`
echo $TAG ;
cd $HOME/devspace/ayi_pub ;
./rocket_pub.sh  --prj rigger-ng  --tag $TAG --host $*
