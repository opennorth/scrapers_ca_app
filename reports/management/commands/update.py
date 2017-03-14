import argparse
import os
import importlib
import logging
import signal
import sys

from django.core.management.base import BaseCommand

import pupa_settings
from reports.utils import scrape

pid = os.getpid()


def signal_handler(signalnum, handler):
    os.kill(pid, signal.SIGKILL)


signal.signal(signal.SIGINT, signal_handler)


class Command(BaseCommand):
    help = 'Scrapes documents for jurisdictions'

    def add_arguments(self, parser):
        parser.add_argument('module', nargs='*')
        parser.add_argument(
            '--fastmode',
            action='store_true',
            dest='fastmode',
            default=False,
            help='Use the cache and turn off throttling.'
        )

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        # @see https://github.com/opencivicdata/pupa/blob/master/pupa/cli/__main__.py
        parser = argparse.ArgumentParser('pupa')
        subparsers = parser.add_subparsers(dest='subcommand')
        subcommand = importlib.import_module('pupa.cli.commands.update').Command(subparsers)

        logging.config.dictConfig(pupa_settings.LOGGING)
        handler = logging.getLogger().handlers[0]
        module_names = options['module'] or os.listdir('scrapers')
        prepend_args = ['update']
        if options['fastmode']:
            prepend_args.append('--fastmode')
        append_args = ['people']

        # @see https://pythonhosted.org//logutils/testing.html
        # @see http://plumberjack.blogspot.ca/2010/09/unit-testing-and-logging.html
        for module_name in module_names:
            if os.path.isfile(os.path.join('scrapers', module_name, '__init__.py')):
                scrape(module_name, parser, subcommand, handler, prepend_args, append_args)
