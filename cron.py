#!/usr/bin/env python
# @see https://github.com/opencivicdata/pupa/blob/master/pupa/cli/__main__.py
import argparse
from datetime import datetime
import os
import importlib
import logging
import sys
import traceback

if __name__ == "__main__":
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapers_ca_app.settings")
  sys.path.append(os.path.abspath('scrapers'))

  from reports.models import Report

  parser = argparse.ArgumentParser('pupa', description='pupa CLI')
  subparsers = parser.add_subparsers(dest='subcommand')
  subcommand = importlib.import_module('pupa.cli.commands.update').Command(subparsers)

  if len(sys.argv) == 1:
    module_names = os.listdir('scrapers')
  else:
    module_names = sys.argv[1:]

  handler = logging.getLogger().handlers[0]

  # @see http://pythonhosted.org//logutils/testing.html
  # @see http://plumberjack.blogspot.ca/2010/09/unit-testing-and-logging.html
  for module_name in module_names:
    if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
      obj, _ = Report.objects.get_or_create(module=module_name)
      try:
        obj.report = subcommand.handle(parser.parse_args(['update', '--nonstrict', '--people', module_name]))
        obj.exception = ''
        obj.success_at = datetime.now()
      except:
        obj.exception = traceback.format_exc()
      obj.warnings = '\n'.join('%(asctime)s %(levelname)s %(name)s: %(message)s' % d for d in handler.buffer)
      obj.save()
      handler.flush()
