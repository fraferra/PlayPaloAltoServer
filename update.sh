TITLE=$1
bash set-time.sh
cd ..
git add .
git commit -m $TITLE
git push origin master
cd django