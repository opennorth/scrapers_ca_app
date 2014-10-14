# coding: utf-8
from __future__ import unicode_literals

import codecs
import cStringIO
import csv
import importlib
import os
import re
from StringIO import StringIO
import sys
from six.moves.urllib.parse import urlsplit

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from pupa.core import _configure_db, db

from reports.models import Report
from reports.utils import get_offices, get_personal_url

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") if s else '' for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class Command(BaseCommand):
  help = 'Generates and uploads CSV files to S3'

  def handle(self, *args, **options):
    def save(key, body):
      k = Key(bucket)
      k.key = key
      k.set_contents_from_string(body)
      k.set_acl('public-read')

    sys.path.append(os.path.abspath('scrapers'))

    url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')
    parsed = urlsplit(url)
    _configure_db(url, parsed.port, parsed.path[1:])

    bucket = S3Connection().get_bucket('represent.opennorth.ca')

    names = {
      'Parliament of Canada': 'house-of-commons',
      'Legislative Assembly of Alberta': 'alberta-legislature',
      'Legislative Assembly of British Columbia': 'bc-legislature',
      'Legislative Assembly of Manitoba': 'manitoba-legislature',
      'Legislative Assembly of New Brunswick': 'new-brunswick-legislature',
      'Newfoundland and Labrador House of Assembly': 'newfoundland-labrador-legislature',
      'Nova Scotia House of Assembly': 'nova-scotia-legislature',
      'Legislative Assembly of Ontario': 'ontario-legislature',
      'Legislative Assembly of Prince Edward Island': 'pei-legislature',
      'Assemblée nationale du Québec': 'quebec-assemblee-nationale',
      'Legislative Assembly of Saskatchewan': 'saskatchewan-legislature',
    }

    default_headers = [
      'District name',
      'Elected office',
      'Name',
      'First name',
      'Last name',
      'Gender',
      'Party name',
      'Email',
      'URL',
      'Photo URL',
      'Personal URL',
      'Facebook',
      'Twitter',
      'YouTube',
    ]
    office_headers = [
      'Office type',
      'Address',
      'Phone',
      'Fax',
    ]

    all_rows = []
    max_offices_count = 0

    reports = Report.objects.filter(exception='').exclude(module__endswith='_candidates').exclude(module__endswith='_municipalities').order_by('module')
    for report in reports:
      try:
        module = importlib.import_module(report.module)
        for obj in module.__dict__.values():
          jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
          if jurisdiction_id:  # We've found the module.
            name = getattr(obj, 'name', None)

            rows = []
            offices_count = 0

            # Exclude party memberships.
            for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id, 'role': {'$nin': ['member', 'candidate']}}):
              organization = db.organizations.find_one({'_id': membership['organization_id']})
              person = db.people.find_one({'_id': membership['person_id']})

              party_membership = db.memberships.find_one({'jurisdiction_id': jurisdiction_id, 'role': 'member', 'person_id': membership['person_id']})
              if party_membership:
                party_name = db.organizations.find_one({'_id': party_membership['organization_id']})['name']
              else:
                party_name = None

              facebook = None
              twitter = None
              youtube = None
              for link in person['links']:
                domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
                if domain == 'facebook.com':
                  facebook = link['url']
                elif domain == 'twitter.com':
                  twitter = link['url']
                elif domain == 'youtube.com':
                  youtube = link['url']

              if person['gender'] == 'male':
                gender = 'M'
              elif person['gender'] == 'female':
                gender = 'F'
              else:
                gender = None

              if ' ' in person['name']:
                first_name, last_name = person['name'].rsplit(' ', 1)
              else:
                first_name, last_name = None, person['name']

              # @see http://represent.opennorth.ca/api/#fields
              row = [
                person['post_id'], # District name
                membership['role'], # Elected office
                person['name'], # Name
                first_name, # First name
                last_name, # Last name
                gender, # Gender
                party_name, # Party name
                next((contact_detail['value'] for contact_detail in membership['contact_details'] if contact_detail['type'] == 'email'), None), # Email
                person['sources'][-1]['url'] if len(person['sources']) > 1 else None, # URL
                person['image'], # Photo URL
                get_personal_url(person), # Personal URL
                facebook, # Facebook
                twitter, # Twitter
                youtube, # YouTube
              ]

              offices = get_offices(membership)
              if len(offices) > offices_count:
                offices_count = len(offices)

              for office in offices:
                for key in ('type', 'postal', 'tel', 'fax'):
                  row.append(office.get(key))

              # If the person is associated to multiple boundaries.
              if re.search(r'\AWards \d(?:(?:,| & | and )\d+)+\Z', person['post_id']):
                for district_id in re.findall(r'\d+', person['post_id']):
                  row = row[:]
                  row[0] = 'Ward %s' % district_id
                  rows.append(row)
              else:
                rows.append(row)

            rows.sort()

            headers = default_headers[:]
            for _ in range(offices_count):
              headers += office_headers

            if name in names:
              slug = names[name]
            else:
              slug = slugify(name)

            io = StringIO()
            body = UnicodeWriter(io, encoding='windows-1252')
            body.writerow(headers)
            body.writerows(rows)
            save('csv/%s.csv' % slug, io.getvalue())

            if offices_count > max_offices_count:
              max_offices_count = offices_count

            for row in rows:
              row.insert(0, name)
              all_rows.append(row)
      except ImportError:
        report.delete()  # delete reports for old modules

    headers = ['Organization'] + default_headers
    for _ in range(max_offices_count):
      headers += office_headers

    io = StringIO()
    body = UnicodeWriter(io, encoding='windows-1252')
    body.writerow(headers)
    body.writerows(all_rows)
    save('csv/complete.csv', io.getvalue())
