from collections import defaultdict
import importlib
import json
import os
import re
import sys
from urlparse import urlsplit

from coffin.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from pupa.core import _configure_db, db
import requests

from reports.models import Report

CONTACT_DETAIL_TYPE_MAP = {
  'address': 'postal',
  'cell': 'alt',
  'fax': 'fax',
  'voice': 'tel',
}

def home(request):
  sys.path.append(os.path.abspath('scrapers'))

  data = json.loads(requests.get('http://represent.opennorth.ca/representative-sets/?limit=0').content)

  names = {}
  for obj in data['objects']:
    names[obj['name']] = obj['data_url']

  icons = {}
  for module_name in os.listdir('scrapers'):
    if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
      module = importlib.import_module(module_name)
      for obj in module.__dict__.values():
        jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
        if jurisdiction_id:  # We've found the module.
          name = getattr(obj, 'name', None)
          if name:
            try:
              if name in names:
                obj = Report.objects.get(module=module_name)
                if not obj.exception:
                  if names[name].startswith('http://scrapers.herokuapp.com/represent/'):
                    icons[obj.id] = 'noop'
                  else:
                    icons[obj.id] = 'replace'
              else:
                obj = Report.objects.get(module=module_name)
                if not obj.exception:
                  icons[obj.id] = 'add'
            except Report.DoesNotExist:
              pass

  return render_to_response('index.html', RequestContext(request, {
    'exceptions': Report.objects.exclude(exception='').count(),
    'reports': Report.objects.order_by('module').all(),
    'icons': icons,
  }))

def report(request, module_name):
  return HttpResponse(json.dumps(Report.objects.get(module=module_name).report), content_type='application/json')

def represent(request, module_name):
  sys.path.append(os.path.abspath('scrapers'))

  url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')
  parsed = urlsplit(url)
  _configure_db(url, parsed.port, parsed.path[1:])

  module = importlib.import_module(module_name)

  for obj in module.__dict__.values():
    jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
    if jurisdiction_id:  # We've found the module.
      representatives = []

      for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id}):
        organization = db.organizations.find_one({'_id': membership['organization_id']})
        person = db.people.find_one({'_id': membership['person_id']})

        # @see http://represent.opennorth.ca/api/#fields
        representative = {
          'name':           person['name'],
          'elected_office': membership['role'],
          'source_url':     person['sources'][0]['url'],
          'email':          next((contact_detail['value'] for contact_detail in membership['contact_details'] if contact_detail['type'] == 'email'), None),
          'photo_url':      person['image'],
          'personal_url':   get_personal_url(person),
          'gender':         person['gender'],
          'offices':        json.dumps(get_offices(membership)),
          'extra':          json.dumps(get_extra(person)),
        }

        if len(person['sources']) > 1:
          representative['url'] = person['sources'][-1]['url']

        geographic_code = getattr(obj, 'geographic_code', None)

        # If the person is associated to multiple boundaries.
        if re.search(r'\AWards \d(?:(?:,| & | and )\d)+\Z', person['post_id']):
          for district_id in re.findall(r'\d+', person['post_id']):
            representative = representative.copy()
            representative['district_id'] = district_id
            representative['district_name'] = 'Ward %s' % district_id
            representatives.append(representative)
        else:
          # If the post_id is numeric.
          if re.search(r'\A\d+\Z', person['post_id']):
            representative['district_id'] = person['post_id']
          # If the post_id is a boundary URL.
          elif re.search(r'\A/boundaries/', person['post_id']):
            representative['boundary_url'] = person['post_id']
          # If the post_id is a census subdivision.
          elif person['post_id'] == getattr(obj, 'division_name', None) and len(str(geographic_code)) == 7:
            representative['district_name'] = person['post_id']
            representative['boundary_url'] = '/boundaries/census-subdivisions/%d/' % geographic_code
          else:
            representative['district_name'] = person['post_id']
            district_id = re.search(r'\A(?:District|Division|Ward) (\d+)\Z', person['post_id'])
            if district_id:
              representative['district_id'] = district_id.group(1)

          representatives.append(representative)

      return HttpResponse(json.dumps(representatives), content_type='application/json')

def get_personal_url(obj):
  for link in obj['links']:
    domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
    if domain not in ('facebook.com', 'twitter.com', 'youtube.com'):
      return link['url']
  return None

def get_offices(obj):
  offices_by_note = defaultdict(dict)
  for contact_detail in obj['contact_details']:
    if contact_detail['type'] != 'email' and contact_detail['note']:
      note = contact_detail['note']
      offices_by_note[note]['type'] = note
      offices_by_note[note][CONTACT_DETAIL_TYPE_MAP[contact_detail['type']]] = contact_detail['value']
  return offices_by_note.values()

def get_extra(obj):
  extra = {}
  for link in obj['links']:
    domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
    if domain == 'facebook.com':
      extra['facebook'] = link['url']
    elif domain == 'twitter.com':
      extra['twitter'] = link['url']
    elif domain == 'youtube.com':
      extra['youtube'] = link['url']
  return extra
