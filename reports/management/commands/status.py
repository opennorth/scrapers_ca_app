import csv
import os
import sys
from io import StringIO

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from opencivicdata.divisions import Division

from reports.models import Report
from reports.utils import module_name_to_metadata


class Command(BaseCommand):
    help = 'Reports statuses of scrapers, with the population as an indication of priority'

    def add_arguments(self, parser):
        parser.add_argument('threshold', nargs='?', type=int)
        parser.add_argument('module', nargs='*')

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        threshold = options['threshold']
        module_names = options['module'] or os.listdir('scrapers')

        # @see http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/index-eng.cfm
        urls = [
            # Provinces and territories
            'http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/Tables/CompFile.cfm?Lang=Eng&T=101&OFT=FULLCSV',
            # Census subdivisions
            'http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/Tables/CompFile.cfm?Lang=Eng&T=701&OFT=FULLCSV',
            # Census divisions
            'http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/Tables/CompFile.cfm?Lang=Eng&T=301&OFT=FULLCSV',
        ]

        populations = {}
        for url in urls:
            response = requests.get(url, verify=settings.SSL_VERIFY)
            response.encoding = 'iso-8859-1'
            reader = csv.DictReader(StringIO(response.text))
            for row in reader:
                if row:
                    populations[row['Geographic code']] = int(row['Population, 2016'] or 0)
                else:
                    break

        for module_name in module_names:
            if os.path.isfile(os.path.join('scrapers', module_name, '__init__.py')):
                division_id = module_name_to_metadata(module_name)['division_id']
                try:
                    report = Report.objects.get(module=module_name)
                    if report.exception:
                        status = 'error'
                    else:
                        status = 'success'
                except Report.DoesNotExist:
                    status = 'unknown'

                sgc = Division.get(division_id).attrs['sgc'] or division_id.rsplit(':', 1)[1]

                population = populations.get(sgc, 0)
                if not threshold or population < threshold:
                    print(f'{module_name:<32} {status:<7} {population:8}')
