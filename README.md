# Canadian Legislative Scrapers

This Django project runs the [Canadian legislative scrapers](http://github.com/opencivicdata/scrapers-ca), displays the status of each scraper, and returns the scraped data as JSON.

## Development

Create a virtual environment:

```
rm -rf ~/.virtualenvs/scrapers_ca_app
mkvirtualenv scrapers_ca_app
pip install -r requirements-dev.txt
```

Create a database:

```
dropdb pupa
createdb pupa
psql pupa -c 'CREATE EXTENSION hstore'
python manage.py syncdb --noinput
```

Run the scrapers:

```
python cron.py
```

Start the web app:

```
foreman start
```

## Deployment

Add a `SECRET_KEY` configuration variable:

```
heroku config:add DJANGO_SECRET_KEY=your-secret-key
```

Run `CREATE EXTENSION hstore` in a PostgreSQL shell:

```
heroku pg:psql DATABASE
```

Add `python cron.py` to the [Heroku Scheduler](https://scheduler.heroku.com/dashboard).

## Bugs? Questions?

This repository is on GitHub: [http://github.com/opennorth/scrapers_ca_app](http://github.com/opennorth/scrapers_ca_app), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
