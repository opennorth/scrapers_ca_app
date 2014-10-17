import argparse
from datetime import datetime
import os
import importlib
import logging
import signal
import sys
import traceback

from django.core.management.base import BaseCommand

import pupa_settings
from reports.models import Report

pid = os.getpid()

def signal_handler(signalnum, handler):
  os.kill(pid, signal.SIGKILL)

signal.signal(signal.SIGINT, signal_handler)

class Command(BaseCommand):
  args = '<module module ...>'
  help = 'Runs Pupa scrapers'

  def handle(self, *args, **options):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapers_ca_app.settings')
    sys.path.append(os.path.abspath('scrapers'))

    # @see https://github.com/opencivicdata/pupa/blob/master/pupa/cli/__main__.py
    parser = argparse.ArgumentParser('pupa', description='pupa CLI')
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommand = importlib.import_module('pupa.cli.commands.update').Command(subparsers)

    logging.config.dictConfig(pupa_settings.LOGGING)
    handler = logging.getLogger().handlers[0]
    module_names = args or os.listdir('scrapers')

    # @see http://pythonhosted.org//logutils/testing.html
    # @see http://plumberjack.blogspot.ca/2010/09/unit-testing-and-logging.html
    for module_name in module_names:
      if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', '_cache', '_data', '__pycache__'):
        obj, _ = Report.objects.get_or_create(module=module_name)
        try:
          obj.report = subcommand.handle(*parser.parse_known_args(['update', '--fastmode', module_name]))
          obj.exception = ''
          obj.success_at = datetime.now()
        except:
          obj.exception = traceback.format_exc()
        obj.warnings = '\n'.join('%(asctime)s %(levelname)s %(name)s: %(message)s' % d for d in handler.buffer)
        obj.save()
        handler.flush()
