import os
import sys

from django.core.management.base import BaseCommand

from reports.utils import flush


class Command(BaseCommand):
    args = '<module module ...>'
    help = 'Deletes documents by jurisdiction'

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        for module_name in args:
            flush(module_name)
