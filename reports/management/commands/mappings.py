import logging
import os.path
import re
from collections import OrderedDict

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from opencivicdata.divisions import Division

log = logging.getLogger(__name__)

numeric_re = re.compile('^[\d.]+$')


class Command(BaseCommand):
    args = '<module>'
    help = 'Generate mappings between boundary sets and divisions'

    def handle(self, *args, **options):
        mappings = {}

        divisions = list(Division.all('ca'))  # cache all divisions
        for obj in requests.get('https://represent.opennorth.ca/boundary-sets/?limit=0').json()['objects']:
            slug = obj['url'].split('/')[2]
            if obj['url'] in ('/boundary-sets/census-divisions/', '/boundary-sets/census-subdivisions/'):
                continue
            if obj['url'] in ('/boundary-sets/federal-electoral-districts/', '/boundary-sets/federal-electoral-districts-next-election/'):
                prefix = 'ocd-division/country:ca/ed:'
                boundary_key = 'external_id'
            else:
                url = 'https://represent.opennorth.ca{}'.format(obj['url'])
                boundary_set = requests.get(url).json()

                if boundary_set['extra'].get('ocd_division'):
                    division_id = boundary_set['extra']['ocd_division']
                elif boundary_set['extra'].get('geographic_code'):
                    geographic_code = boundary_set['extra']['geographic_code']
                    geographic_code_length = len(geographic_code)
                    if geographic_code_length == 7:
                        division_id = 'ocd-division/country:ca/csd:{}'.format(geographic_code)
                    elif geographic_code_length == 4:
                        division_id = 'ocd-division/country:ca/cd:{}'.format(geographic_code)
                    elif geographic_code_length == 2:
                        division_id = next((division for division in divisions if division.attrs['sgc'] == geographic_code), None).id
                    else:
                        log.error('Unrecognized geographic_code {}'.format(geographic_code))
                        continue

                try:
                    division = Division.get(division_id)
                    if division._type == 'borough':
                        division = division.parent
                        division_id = division.id
                        exclude = ('place', 'borough')
                    elif 'boroughs' in obj['name']:
                        exclude = ('place', 'district')
                    elif 'districts' in obj['name']:
                        exclude = ('place', 'borough')
                    else:
                        exclude = ('place',)

                    subtypes = set(child._type for child in division.children() if child._type not in exclude)
                    if len(subtypes) == 0:
                        log.warn('No subtypes for {}'.format(division_id))
                        continue
                    elif len(subtypes) > 1:
                        log.warn('>1 subtypes for {}: {}'.format(division_id, list(subtypes)))
                        continue
                    else:
                        prefix = '{}/{}:'.format(division_id, subtypes.pop())

                    boundary_key = 'external_id'
                    for child in division.children():
                        if child._type not in exclude:
                            type_id = child.id.rsplit(':', 1)[1]
                            if not numeric_re.search(type_id):
                                if len(type_id) in (1, 3):  # Lunenburg 1-letter identifiers, BC uses 3-letter identifiers
                                    boundary_key = 'lower'
                                else:
                                    boundary_key = 'matcher'
                                break
                except KeyError:
                    log.warn('No division for {}'.format(url))

            mappings[slug] = {
                'key': 'id',
                'prefix': prefix,
                'boundary_key': boundary_key,
            }

        with open(os.path.join(settings.BASE_DIR, 'mappings.py'), 'w') as f:
            f.write("# DO NOT EDIT THIS AUTO-GENERATED FILE\n")
            f.write("import re\n\n")

            f.write("from django.template.defaultfilters import slugify\n\n")

            f.write("leading_zero_re = re.compile(r'^0+')\n")
            f.write("invalid_re = re.compile(r'[^a-z\d._~-]')\n")
            f.write("leading_district_re = re.compile(r'^District ')\n")
            f.write("lower = lambda boundary: boundary['external_id'].lower()\n\n")
            f.write("matcher = lambda boundary: leading_district_re.sub('', leading_zero_re.sub('', invalid_re.sub('~', boundary['name'].lower().replace(' ', '_'))))\n\n")

            f.write('IMAGO_BOUNDARY_MAPPINGS = {\n')
            for slug, data in OrderedDict(sorted(mappings.items())).items():
                f.write("    '{}': {{\n".format(slug))
                for key, value in OrderedDict(sorted(data.items())).items():
                    if key == 'boundary_key' and value in ('lower', 'matcher'):
                        f.write("        '{}': {},\n".format(key, value))
                    else:
                        f.write("        '{}': '{}',\n".format(key, value))
                f.write("    },\n")
            f.write('}\n')
