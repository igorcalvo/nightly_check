echo "*** This could potentially replace your data with outdated data ***"
read -p "Proceed anyway? Type lowercase y: " reply
if test $reply = "y"
then
    empty=""
    backup="backup\/*"
    base_path=$(realpath $(dirname $0))
    from_path=$(echo "$base_path" | sed "s/scripts/backup/")
    from_path=$(echo "$from_path" | sed "s/backup/$backup/")
    dest_path=$(echo "$base_path" | sed "s/scripts/$empty/")

    cp -r $from_path $dest_path
    echo "Data sucessfully restored."
else 
    echo "Nothing was done. Exiting"
fi
