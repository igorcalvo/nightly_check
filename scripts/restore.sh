echo "*** This could potentially replace your data with outdated data ***"
read -p "Proceed anyway? Type lowercase y: " reply
if test $reply = "y"
then
cp -r $(pwd)/../backup/* $(pwd)/../
    echo "Data sucessfully restored."
else 
    echo "Nothing was done. Exiting"
fi
