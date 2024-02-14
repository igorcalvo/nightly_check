# sh Code/NightlyCheck/scripts/backup.sh /home/calvo/Code/NightlyCheck/
cp -r $1data/ $1backup/
cp $1settings.json $1backup/
cp $1variables.csv $1backup/
