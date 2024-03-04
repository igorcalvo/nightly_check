echo "*** THIS IS GOING TO DELETE YOUR DATA ***"
echo "Consider making a backing up your data first"
read -p "Are you sure? Type lowercase y: " reply
if test $reply = "y"
then
    base_path=$(realpath $(dirname $0))
    dest_path=$(echo "$base_path" | sed "s/scripts/data/")

    rm -r $dest_path
    echo "Data sucessfully deleted."
else 
    echo "Nothing was done. Exiting"
fi

