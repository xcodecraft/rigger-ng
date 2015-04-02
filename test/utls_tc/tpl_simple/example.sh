echo "this is rg tpl"
echo "Hi,%{YOUNAME}"
echo "love rg?"
#% T.LOVE : {
echo "love you too! "
#% }
#% T.DB == "mysql" : {
echo "mysql is free! "
#% }
#% T.DB == "orcal" : {
echo "you are tuhao!"
#% }
