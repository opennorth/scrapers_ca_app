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

# @todo check all link note values
PERSONAL_URL_NOTES = ('personal site', 'web page', 'Website')

# @todo check all contact detail type values
CONTACT_DETAIL_TYPE_MAP = {
  'voice': 'tel',
  'address': 'postal',
  'fax': 'fax',
}

def home(request):
  return render_to_response('index.html', RequestContext(request, {
    'reports': Report.objects.all(),
  }))

def represent(request, module_name):
  url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')
  parsed = urlsplit(url)
  _configure_db(url, parsed.port, parsed.path[1:])

  sys.path.append(os.path.abspath('scrapers'))
  module = importlib.import_module(module_name)

  for obj in module.__dict__.values():
    jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
    if jurisdiction_id:  # We've found the module.
      data = []

      # @todo check that all people are plain members of jurisdictions, without duplicates
      for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id, 'role': 'member'}):
        organization = db.organizations.find_one({'_id': membership['organization_id']})
        person = db.people.find_one({'_id': membership['person_id']})

        role = db.memberships.find_one({'person_id': membership['person_id'], 'role': {'$ne': 'member'}})
        if role:
          role = role['role'] # @todo check that role['role'] is not empty
        else:
          role = 'councillor' # @todo warn or error

        data.append({
          'name':           person['name'],
          # @todo check
          'district_name':  organization['name'] + ' ' + person['post_id'],
          'elected_office': role,
          'source_url':     person['sources'][0]['url'],
          # @todo check that contact details are on the membership in all cases
          'email':          next(contact_detail['value'] for contact_detail in membership['contact_details'] if contact_detail['type'] == 'email', None),
          'url':            person['sources'][-1]['url'],
          'photo_url':      person['image'],
          # @todo check that links are on the person in all cases
          'personal_url':   next(link['url'] for link in person['links'] if link['note'] in PERSONAL_URL_NOTES, None),
          # @todo check
          'district_id':    person['post_id'],
          'gender':         person['gender'],
          'offices':        get_offices(membership),
          'extra':          get_extra(person),
        })

      return HttpResponse(json.dumps(data), mimetype='application/json')

# @todo check all contact detail note values
def get_offices(obj):
  offices_by_note = defaultdict(dict)
  for contact_detail in obj['contact_details']:
    # @todo skip if note is empty?
    note = contact_detail['note']
    offices_by_note[note]['type'] = note
    offices_by_note[note][CONTACT_DETAIL_TYPE_MAP[contact_detail['type']]] = contact_detail['value']
  return offices_by_note.values()

def get_extra(obj):
  extra = {}
  for link in obj['links']:
    if link['note'] not in PERSONAL_URL_NOTES:
      extra[link['note']] = link['url']
  return extra
