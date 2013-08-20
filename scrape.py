
import sys, os
import importlib
import argparse
from mycityhall_scrapers import scrape
from pupa.cli import __main__
from pupa.cli.commands import update, base
from reports.models import Report


if len(sys.argv) == 0:
  reports = scrape.scrape_people()
  reports = reports + scrape.scrape_events()
else:
  if sys.argv[0] == 'people':
    reports = scrape.scrape_people()
  if sys.argv[0] == 'events':
    reports = scrape.scrape_events()
reports = scrape.scrape_people()
Report.objects.all().delete()
for report in reports:
  r = Report(name=report['name'], status=report['status'], error=report['error'])
  r.save()

