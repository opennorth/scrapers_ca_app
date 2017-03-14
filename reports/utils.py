import logging
import importlib
import re
import traceback
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlsplit

from django.db import transaction
from django.db.models import Count
from opencivicdata.models import Jurisdiction, Membership, Organization, Person, Post

from reports.models import Report

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


def scrape(module_name, parser, subcommand, handler, prepend_args, append_args):
    report, _ = Report.objects.get_or_create(module=module_name)
    try:
        with transaction.atomic():
            flush(module_name)
            known_args = prepend_args[:]
            known_args.append(module_name)
            known_args.extend(append_args)
            args, other = parser.parse_known_args(known_args)
            report.report = subcommand.handle(args, other)
            report.exception = ''
            report.success_at = datetime.now()
    except:
        report.exception = traceback.format_exc()
    report.warnings = '\n'.join('%(asctime)s %(levelname)s %(name)s: %(message)s' % d for d in handler.buffer if ' memberships, ' not in d['message'])
    report.save()
    handler.flush()


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
        parties_count = qs.count()
        qs.delete()

        # Delete organizations.
        qs = Organization.objects.filter(jurisdiction_id=jurisdiction_id)
        organizations_count = qs.count()
        qs.delete()

        log.info("{}: {} people, {} memberships, {} posts, {} parties, {} organizations".format(jurisdiction_id, people_count, memberships_count, posts_count, parties_count, organizations_count))
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
