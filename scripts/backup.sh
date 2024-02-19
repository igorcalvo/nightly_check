# sh Code/NightlyCheck/scripts/backup.sh /home/calvo/Code/NightlyCheck/
cp -r $1data/ $1backup/
echo "Done. Data saved in $1backup/"
