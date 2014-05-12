from collections import defaultdict
from urlparse import urlsplit

CONTACT_DETAIL_TYPE_MAP = {
  'address': 'postal',
  'cell': 'alt',
  'fax': 'fax',
  'voice': 'tel',
}

def get_offices(obj):
  offices_by_note = defaultdict(dict)
  for contact_detail in obj['contact_details']:
    if contact_detail['type'] != 'email' and contact_detail['note']:
      note = contact_detail['note']
      offices_by_note[note]['type'] = note
      offices_by_note[note][CONTACT_DETAIL_TYPE_MAP[contact_detail['type']]] = contact_detail['value']
  return list(offices_by_note.values())

def get_personal_url(obj):
  for link in obj['links']:
    domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
    if domain not in ('facebook.com', 'twitter.com', 'youtube.com'):
      return link['url']
  return None

