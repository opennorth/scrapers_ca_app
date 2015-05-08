import logging
import importlib
import re
from collections import defaultdict

from opencivicdata.models import Jurisdiction, Person, Post
from six.moves.urllib.parse import urlsplit

CONTACT_DETAIL_TYPE_MAP = {
    'address': 'postal',
    'cell': 'alt',
    'fax': 'fax',
    'voice': 'tel',
}

log = logging.getLogger(__name__)

remove_suffix_re = re.compile(r' \(\D[^)]+\)\Z')


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
        if domain not in ('facebook.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com'):
            return link.url
    return None


def flush(module_name):
    try:
        division_id = module_name_to_division_id(module_name)
        jurisdiction_id = '{}/{}'.format(division_id.replace('ocd-division', 'ocd-jurisdiction'), 'legislature')
        qs = Person.objects.filter(memberships__organization__jurisdiction_id=jurisdiction_id)
        people_count = qs.count()
        qs.delete()  # cascades Membership
        qs = Post.objects.filter(organization__jurisdiction_id=jurisdiction_id)
        posts_count = qs.count()
        qs.delete()
        log.info("%s: %d people, %d posts" % (jurisdiction_id, people_count, posts_count))
    except Jurisdiction.DoesNotExist:
        log.error("No Jurisdiction with id='%s'" % jurisdiction_id)


def module_name_to_division_id(module_name):
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
        division_id = getattr(obj, 'division_id', None)
        if division_id:
            return division_id
