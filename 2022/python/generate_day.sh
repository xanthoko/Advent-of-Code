padded_day=$(seq -f "%02g" $1 $1)

cp template.py day$padded_day.py
sed -i '' "s/dayOfInput/$1/" day$padded_day.py

python utils.py $1
