metanews
========

for now, scrape huffpo front page find authors and classify them as male or female

python manage.py scrape_huffpo

you may have to run python manage.py shell -> from metanews.apps.classifier.USSSALoader import getNameList;getNameList()

python manage.py print_authors

inspired by http://whowritesfor.com/
