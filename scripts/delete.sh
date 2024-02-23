echo "*** THIS IS GOING TO DELETE YOUR DATA ***"
echo "Consider making a backing up your data first"
read -p "Are you sure? Type lowercase y: " reply
if test $reply = "y"
then
    rm -r $(pwd)/../data/
    echo "Data sucessfully deleted."
else 
    echo "Nothing was done. Exiting"
fi

