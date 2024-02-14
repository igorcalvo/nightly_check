# sh Code/NightlyCheck/scripts/delete.sh /home/calvo/Code/NightlyCheck/
echo "*** THIS IS GOING TO DELETE YOUR DATA ***"
echo "Consider making a backing up your data first"
read -p "Are you sure? Type lowercase y: " reply
if test $reply = "y"
then
    rm -r $1data/
    rm $1settings.json
    rm $1variables.csv
    echo "Data sucessfully deleted."
else 
    echo "Nothing was done. Exiting"
fi

