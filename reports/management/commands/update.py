import argparse
import os
import importlib
import logging
import signal
import sys
import traceback
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import transaction

import pupa_settings
from reports.models import Report
from reports.utils import flush

pid = os.getpid()


def signal_handler(signalnum, handler):
    os.kill(pid, signal.SIGKILL)

signal.signal(signal.SIGINT, signal_handler)


class Command(BaseCommand):
    args = '<module module ...>'
    help = 'Scrapes documents for jurisdictions'
    option_list = BaseCommand.option_list + (
        make_option('--fastmode', action='store_true', dest='fastmode',
                    default=False,
                    help='Use the cache and turn off throttling.'),
    )

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        # @see https://github.com/opencivicdata/pupa/blob/master/pupa/cli/__main__.py
        parser = argparse.ArgumentParser('pupa')
        subparsers = parser.add_subparsers(dest='subcommand')
        subcommand = importlib.import_module('pupa.cli.commands.update').Command(subparsers)

        logging.config.dictConfig(pupa_settings.LOGGING)
        handler = logging.getLogger().handlers[0]
        module_names = args or os.listdir('scrapers')
        prepend_args = ['update']
        if options['fastmode']:
            prepend_args.append('--fastmode')
        append_args = ['people']

        # @see https://pythonhosted.org//logutils/testing.html
        # @see http://plumberjack.blogspot.ca/2010/09/unit-testing-and-logging.html
        for module_name in module_names:
            if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', '_cache', '_data', '__pycache__', 'disabled'):
                report, _ = Report.objects.get_or_create(module=module_name)
                try:
                    with transaction.atomic():
                        flush(module_name)
                        known_args = prepend_args[:]
                        known_args.append(module_name)
                        known_args.extend(append_args)
                        args, other = parser.parse_known_args(known_args)
                        report.report = subcommand.handle(args, other)
                        report.exception = ''
                        report.success_at = datetime.now()
                except:
                    report.exception = traceback.format_exc()
                report.warnings = '\n'.join('%(asctime)s %(levelname)s %(name)s: %(message)s' % d for d in handler.buffer if ' memberships, ' not in d['message'])
                report.save()
                handler.flush()
