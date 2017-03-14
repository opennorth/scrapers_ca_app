import os
import signal
import sys

from django.core.management.base import BaseCommand

from reports.utils import scrape_configuration, scrape_people

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

        parser, subcommand, handler = scrape_configuration()

        module_names = options['module'] or os.listdir('scrapers')

        if options['fastmode']:
            extra_args = ['--fastmode']
        else:
            extra_args = []

        # @see https://pythonhosted.org//logutils/testing.html
        # @see http://plumberjack.blogspot.ca/2010/09/unit-testing-and-logging.html
        for module_name in module_names:
            if os.path.isfile(os.path.join('scrapers', module_name, '__init__.py')):
                scrape_people(module_name, parser, subcommand, handler, extra_args)
