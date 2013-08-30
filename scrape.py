
import sys, os
import importlib
import argparse
from mycityhall_scrapers import scrape, export_represent
from pupa.cli import __main__
from pupa.cli.commands import update, base
from reports.models import Report

print sys.argv

if len(sys.argv) == 1:
  reports = scrape.scrape_people()
  reports = reports + scrape.scrape_events()
else:
  if sys.argv[1] == 'people':
    reports = scrape.scrape_people()
  if sys.argv[1] == 'events':
    reports = scrape.scrape_events()
export_represent.main()
Report.objects.all().delete()
for report in reports:
  r = Report(name=report['name'], status=report['status'], error=report['error'])
  r.save()

