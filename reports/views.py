import importlib
import json
import os
import re
import sys
from six.moves.urllib.parse import urlsplit

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from pupa.core import _configure_db, db
import requests

from reports.models import Report
from reports.utils import get_offices, get_personal_url

def home(request):
  sys.path.append(os.path.abspath('scrapers'))

  data = json.loads(requests.get('http://represent.opennorth.ca/representative-sets/?limit=0').text)

  names = {}
  for obj in data['objects']:
    if obj['name'] == 'House of Commons':
      names['Parliament of Canada'] = obj['data_url']
    else:
      names[obj['name']] = obj['data_url']

  reports = Report.objects.order_by('module').all()
  for report in reports:
    if not report.exception:
      try:
        module = importlib.import_module(report.module)
        for obj in module.__dict__.values():
          jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
          if jurisdiction_id:  # We've found the module.
            name = getattr(obj, 'name', None)
            if name in names:
              if names[name].startswith('http://scrapers.herokuapp.com/represent/'):
                report.icon = 'noop'
              else:
                report.icon = 'replace'
            else:
              report.icon = 'add'
      except ImportError:
        report.delete()  # delete reports for old modules

  return render_to_response('index.html', RequestContext(request, {
    'exceptions': Report.objects.exclude(exception='').count(),
    'reports': reports,
  }))

def warnings(request):
  return render_to_response('warnings.html', RequestContext(request, {
    'reports': Report.objects.order_by('module').all(),
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

      # Exclude party memberships.
      criteria = {'jurisdiction_id': jurisdiction_id}

      if module_name.endswith('_candidates'):
        criteria['role'] = 'candidate'
      else:
        criteria['role'] = {'$nin': ['member', 'candidate']}

      for membership in db.memberships.find(criteria):
        organization = db.organizations.find_one({'_id': membership['organization_id']})
        person = db.people.find_one({'_id': membership['person_id']})

        party_membership = db.memberships.find_one({'jurisdiction_id': jurisdiction_id, 'role': 'member', 'person_id': membership['person_id']})
        if party_membership:
          party_name = db.organizations.find_one({'_id': party_membership['organization_id']})['name']
        else:
          party_name = None

        if person['gender'] == 'male':
          gender = 'M'
        elif person['gender'] == 'female':
          gender = 'F'
        else:
          gender = None

        # @see http://represent.opennorth.ca/api/#fields
        representative = {
          'name':           person['name'],
          'elected_office': membership['role'],
          'party_name':     party_name,
          'email':          next((contact_detail['value'] for contact_detail in membership['contact_details'] if contact_detail['type'] == 'email'), None),
          'photo_url':      person['image'],
          'personal_url':   get_personal_url(person),
          'gender':         gender,
          'offices':        json.dumps(get_offices(membership)),
          'extra':          json.dumps(get_extra(person)),
        }

        # @see https://github.com/opennorth/represent-canada/issues/81
        if len(person['sources'][0]['url']) <= 200:
          representative['source_url'] = person['sources'][0]['url']

        if len(person['sources']) > 1:
          representative['url'] = person['sources'][-1]['url']

        # If the person is associated to multiple boundaries.
        if re.search(r'\AWards \d(?:(?:,| & | and )\d+)+\Z', person['post_id']):
          for district_id in re.findall(r'\d+', person['post_id']):
            representative = representative.copy()
            representative['district_id'] = district_id
            representative['district_name'] = 'Ward %s' % district_id
            representatives.append(representative)
        else:
          geographic_code = getattr(obj, 'geographic_code', None)
          # If the post_id is numeric.
          if re.search(r'\A\d+\Z', person['post_id']):
            representative['district_id'] = person['post_id']
          # If the person has a boundary URL.
          elif person.get('extras', {}).get('boundary_url'):
            representative['district_name'] = person['post_id']
            representative['boundary_url'] = person['extras']['boundary_url']
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

def get_extra(obj):
  extra = obj.get('extras', {})
  for link in obj['links']:
    domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
    if domain == 'facebook.com':
      extra['facebook'] = link['url']
    elif domain == 'twitter.com':
      extra['twitter'] = link['url']
    elif domain == 'youtube.com':
      extra['youtube'] = link['url']
  return extra
