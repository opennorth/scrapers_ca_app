from collections import defaultdict
import importlib
import json
import os
import sys
from urlparse import urlsplit

from coffin.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from pupa.core import _configure_db, db
from reports.models import Report

CONTACT_DETAIL_TYPE_MAP = {
  'address': 'postal',
  'cell': 'alt',
  'fax': 'fax',
  'voice': 'tel',
}

def home(request):
  return render_to_response('index.html', RequestContext(request, {
    'exceptions': Report.objects.exclude(exception='').count(),
    'reports': Report.objects.order_by('module').all(),
  }))

def report(request, module_name):
  return HttpResponse(json.dumps(Report.objects.get(module=module_name).report), content_type='application/json')

def represent(request, module_name):
  url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')
  parsed = urlsplit(url)
  _configure_db(url, parsed.port, parsed.path[1:])

  sys.path.append(os.path.abspath('scrapers'))
  module = importlib.import_module(module_name)

  for obj in module.__dict__.values():
    jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
    if jurisdiction_id:  # We've found the module.
      representatives = []

      for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id}):
        organization = db.organizations.find_one({'_id': membership['organization_id']})
        person = db.people.find_one({'_id': membership['person_id']})

        # @see http://represent.opennorth.ca/api/#fields
        representatives.append({
          'name':           person['name'],
          'district_name':  person['post_id'], # @todo remove post_id and instead use a field in 'extra'
          'elected_office': membership['role'],
          'source_url':     person['sources'][0]['url'],
          'email':          next((contact_detail['value'] for contact_detail in membership['contact_details'] if contact_detail['type'] == 'email'), None),
          'url':            person['sources'][-1]['url'],
          'photo_url':      person['image'],
          'personal_url':   get_personal_url(person),
          'district_id':    person['post_id'], # @todo remove post_id and instead use a field in 'extra'
          'gender':         person['gender'],
          'offices':        json.dumps(get_offices(membership)),
          'extra':          json.dumps(get_extra(person)),
        })

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
