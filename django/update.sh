TITLE=$1
cd ..
git add .
git commit -m $TITLE
git push origin master
cd django