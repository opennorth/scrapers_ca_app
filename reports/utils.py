import re
from collections import defaultdict

from six.moves.urllib.parse import urlsplit

CONTACT_DETAIL_TYPE_MAP = {
    'address': 'postal',
    'cell': 'alt',
    'fax': 'fax',
    'voice': 'tel',
}

remove_suffix_re = re.compile(r' \([^)]+\)\Z')


def get_offices(record):
    offices_by_note = defaultdict(dict)
    for contact_detail in record.contact_details.all():
        if contact_detail.type != 'email' and contact_detail.note:
            note = contact_detail.note
            offices_by_note[note]['type'] = note.partition(' ')[0]
            offices_by_note[note][CONTACT_DETAIL_TYPE_MAP[contact_detail.type]] = contact_detail.value
    return list(offices_by_note.values())


def get_personal_url(record):
    for link in record.links.all():
        domain = '.'.join(urlsplit(link.url).netloc.split('.')[-2:])
        if domain not in ('facebook.com', 'linkedin.com', 'twitter.com', 'youtube.com'):
            return link.url
    return None
