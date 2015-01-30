import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from opencivicdata.divisions import Division

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<module>'
    help = 'Check mappings between remote boundary sets and divisions'

    def handle(self, *args, **options):
        ids = set(division.id for division in Division.all('ca'))
        for slug, data in settings.IMAGO_BOUNDARY_MAPPINGS.items():
            url = 'https://represent.opennorth.ca/boundaries/{}/?limit=0'.format(slug)
            for obj in requests.get(url).json()['objects']:
                if callable(data['boundary_key']):
                    expected = data['prefix'] + data['boundary_key'](obj)
                else:
                    expected = data['prefix'] + obj[data['boundary_key']]
                if expected not in ids:
                    log.warn('No match for {} from {}'.format(expected, url))
