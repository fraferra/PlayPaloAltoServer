TITLE=$1
bash set-time.sh

git add .
git commit -m $TITLE
git push origin master
git push heroku-fra master
git push heroku master
