base_path=$(realpath $(dirname $0))
from_path=$(echo "$base_path" | sed "s/scripts/data/")
dest_path=$(echo "$base_path" | sed "s/scripts/backup/")

cp -r $from_path $dest_path
echo "Done. Data saved in $dest_path"
