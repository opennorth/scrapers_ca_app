import csv
import os
import sys

import requests
from django.core.management.base import BaseCommand
from six import StringIO

from reports.models import Report
from reports.utils import module_name_to_division_id

class Command(BaseCommand):
    args = '<module module ...>'
    help = 'Reports statuses of scrapers'

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        module_names = args or os.listdir('scrapers')

        populations = {}
        response = requests.get('http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV')
        response.encoding = 'ISO-8859-1'
        reader = csv.reader(StringIO(response.text))
        next(reader)  # title
        next(reader)  # headers
        for row in reader:
            if row:
                populations[row[0]] = int(row[4] or 0)
            else:
                break

        for module_name in module_names:
            if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', '_cache', '_data', '__pycache__', 'disabled'):
                identifier = module_name_to_division_id(module_name).rsplit('/', 1)[-1].split(':', 1)[-1]
                if identifier == 'ca':
                    identifier = '01'
                try:
                    report = Report.objects.get(module=module_name)
                    if report.exception:
                        status = 'error'
                    else:
                        status = 'success'
                except Report.DoesNotExist:
                    status = 'unknown'
                population = populations.get(identifier, 0)
                if population < 50000:
                    print('%-32s %-7s %8d' % (module_name, status, population))
