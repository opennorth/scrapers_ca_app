# Canadian Legislative Scrapers

This Django project runs the [Canadian legislative scrapers](http://github.com/opencivicdata/scrapers-ca), displays the status of each scraper, and returns the scraped data as JSON.

## Development

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/opennorth.ca/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, MongoDB, Python and virtualenv.

    mkvirtualenv scrapers_ca_app
    git clone git@github.com:opennorth/scrapers_ca_app.git
    cd scrapers_ca_app

Set up the submodule and switch it to master:

    git submodule init
    git submodule update
    cd scrapers
    git checkout master
    cd ..

Install the requirements:

    pip install -r requirements.txt

Create a database (`dropdb pupa` if it already exists):

    dropdb pupa
    createdb pupa
    python manage.py syncdb --noinput

Drop the MongoDB database:

    mongo pupa --eval 'db.dropDatabase()'

Run all the scrapers:

    python cron.py

Or run specific scrapers:

    python cron.py ca_ab_edmonton ca_ab_grande_prairie_county_no_1

Install the foreman gem:

    gem install foreman

Start the web app:

    foreman start

## Data Quality

    mkdir test

    mongo pupa sanity/common.js sanity/contact_details.js > test/contact_details.txt
    mongo pupa sanity/common.js sanity/names.js sanity/posts.js sanity/styles.js sanity/miscellaneous.js > test/miscellaneous.txt
    mongo pupa sanity/common.js sanity/relations.js > test/relations.txt
    mongo pupa sanity/common.js sanity/styles.js sanity/roles.js > test/roles.txt

    diff -U0 sanity/pass/contact_details.txt test/contact_details.txt
    diff -U0 sanity/pass/links.txt test/links.txt
    diff -U0 sanity/pass/relations.txt test/relations.txt
    diff -U0 sanity/pass/roles.txt test/roles.txt
    cat test/miscellaneous.txt

## Deployment

Add configuration variables (replace `YOUR-SECRET-KEY` and `DATABASE`):

    heroku config:set PRODUCTION=1
    heroku config:set DJANGO_SECRET_KEY=YOUR-SECRET-KEY
    heroku config:set DATABASE_URL=`heroku config:get DATABASE`

You can [generate a secret key in Python](https://github.com/django/django/blob/master/django/core/management/commands/startproject.py):

```python
from django.utils.crypto import get_random_string
get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
```

Setup the database (replace `DATABASE`):

    heroku pg:reset DATABASE
    heroku run python manage.py syncdb --noinput

Add `python cron.py` to the [Heroku Scheduler](https://scheduler.heroku.com/dashboard).

## Troubleshooting

* Make sure PostgreSQL and MongoDB are running. If you use Homebrew, you can find instructions on how to run each with:

    brew info postgres
    brew info mongo

## Bugs? Questions?

This repository is on GitHub: [http://github.com/opennorth/scrapers_ca_app](http://github.com/opennorth/scrapers_ca_app), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
