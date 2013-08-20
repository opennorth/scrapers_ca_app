
import sys, os
import importlib
import argparse
from mycityhall_scrapers import scrape_people
from pupa.cli import __main__
from pupa.cli.commands import update, base
from reports.models import Report

reports = scrape_people.scrape_people()
Report.objects.all().delete()
for report in reports:
  r = Report(name=report['name'], status=report['status'], error=report['error'])
  r.save()

