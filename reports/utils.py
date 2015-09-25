import logging
import importlib
import re
from collections import defaultdict

from django.db.models import Count
from opencivicdata.models import Jurisdiction, Membership, Organization, Person, Post
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
        if domain not in ('facebook.com', 'fb.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com'):
            return link.url
    return None


def flush(module_name):
    try:
        jurisdiction_id = module_name_to_metadata(module_name)['jurisdiction_id']

        qs = Membership.objects.filter(organization__jurisdiction_id=jurisdiction_id)

        if module_name.endswith('_candidates'):
            qs.filter(role='candidate')
        else:
            qs.exclude(role__in=('member', 'candidate'))

        memberships_count = qs.count()
        qs.delete()

        qs = Post.objects.filter(organization__jurisdiction_id=jurisdiction_id)
        posts_count = qs.count()
        qs.delete()

        people_count = 0

        # Get IDs of people with party memberships.
        ids = Person.objects.filter(memberships__organization__jurisdiction_id=None).values_list('id', flat=True)
        # Get IDs of people with only party memberships.
        ids = Person.objects.values('id').filter(id__in=ids).annotate(count=Count('memberships')).filter(count=1).values_list('id', flat=True)

        # Delete people with only party memberships.
        qs = Person.objects.filter(id__in=ids)
        people_count += qs.count()
        qs.delete()

        # Delete people without memberships.
        qs = Person.objects.filter(memberships__id=None)
        people_count += qs.count()
        qs.delete()

        # Delete parties without members.
        qs = Organization.objects.filter(jurisdiction_id=None, memberships__id=None)
        organization_count = qs.count()
        qs.delete()

        log.info("{}: {} people, {} memberships, {} posts, {} parties".format(jurisdiction_id, people_count, memberships_count, posts_count, organization_count))
    except Jurisdiction.DoesNotExist:
        log.error("No Jurisdiction with id='{}'".format(jurisdiction_id))


def module_name_to_metadata(module_name):
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
        division_id = getattr(obj, 'division_id', None)
        if division_id:
            return {
                'division_id': division_id,
                'division_name': getattr(obj, 'division_name', None),
                'name': getattr(obj, 'name', None),
                'url': getattr(obj, 'url', None),
                'classification': getattr(obj, 'classification', None),
                'jurisdiction_id': '{}/{}'.format(division_id.replace('ocd-division', 'ocd-jurisdiction'), getattr(obj, 'classification', 'legislature')),
            }
