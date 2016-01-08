import csv
import os
import sys

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from opencivicdata.divisions import Division
from six import StringIO

from reports.models import Report
from reports.utils import module_name_to_metadata


class Command(BaseCommand):
    args = '<population-threshold module module ...>'
    help = 'Reports statuses of scrapers, with the population as an indication of priority'

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        args = list(args)
        threshold = args and int(args.pop(0))
        module_names = args or os.listdir('scrapers')

        urls = [
            # Provinces and territories
            'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=101&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-101.CSV',
            # Census subdivisions
            'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=701&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-701.CSV',
            # Census divisions
            'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV',
        ]

        populations = {}
        for url in urls:
            response = requests.get(url, verify=settings.SSL_VERIFY)
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
                division_id = module_name_to_metadata(module_name)['division_id']
                try:
                    report = Report.objects.get(module=module_name)
                    if report.exception:
                        status = 'error'
                    else:
                        status = 'success'
                except Report.DoesNotExist:
                    status = 'unknown'

                sgc = Division.get(division_id).attrs['sgc'] or division_id.rsplit('/', 1)[-1].split(':', 1)[-1]
                if sgc == 'ca':
                    sgc = '01'

                population = populations.get(sgc, 0)
                if not threshold or population < threshold:
                    print('{:<32} {:<7} {:8}'.format(module_name, status, population))
