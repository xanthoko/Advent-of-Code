cp template.py day$1.py

curl "https://adventofcode.com/2021/day/$1/input" \
  -H "cookie: session=53616c7465645f5f2c78c10057f268e297c87f97d34c6c09f6cf7237120c40c0f9555d435e5c3d403717b733a1fcfbdc" \
  --compressed > ../inputs/day$1.txt
