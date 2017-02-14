import os
import sys

from django.core.management.base import BaseCommand

from reports.utils import flush


class Command(BaseCommand):
    help = 'Deletes documents by jurisdiction'

    def add_arguments(self, parser):
        parser.add_argument('module', nargs='+')

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        for module_name in options['module']:
            flush(module_name)
