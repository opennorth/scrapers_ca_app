import json
import os
import re
import sys
from urllib.parse import urlsplit

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from opencivicdata.models import Division, Membership

from reports.models import Report
from reports.utils import get_offices, get_personal_url, module_name_to_metadata, remove_suffix_re


def home(request):
    sys.path.append(os.path.abspath('scrapers'))

    data = json.loads(requests.get('https://represent.opennorth.ca/representative-sets/?limit=0', verify=settings.SSL_VERIFY).text)

    names = {}
    for obj in data['objects']:
        # The `ca` scraper has "Parliament of Canada" as the root organization.
        if obj['name'] == 'House of Commons':
            names['Parliament of Canada'] = obj['data_url']
        else:
            names[obj['name']] = obj['data_url']

    reports = Report.objects.order_by('module').all()
    for report in reports:
        try:
            name = module_name_to_metadata(report.module)['name']
            if not report.exception:
                if name in names:
                    if names[name].startswith('https://scrapers.herokuapp.com/represent/'):
                        report.icon = 'noop'
                    else:
                        report.icon = 'replace'
                else:
                    report.icon = 'add'
        except ImportError:
            report.delete()  # delete reports for old modules

    return render(request, 'index.html', {
        'exceptions': Report.objects.exclude(exception='').count(),
        'reports': reports,
    })


def warnings(request):
    return render(request, 'warnings.html', {
        'reports': Report.objects.order_by('module').all(),
    })


def report(request, module_name):
    return HttpResponse(json.dumps(Report.objects.get(module=module_name).report), content_type='application/json')


def represent(request, module_name):
    sys.path.append(os.path.abspath('scrapers'))

    metadata = module_name_to_metadata(module_name)

    representatives = []

    # Exclude party memberships.
    queryset = Membership.objects.filter(organization__jurisdiction_id=metadata['jurisdiction_id'])

    if module_name.endswith('_candidates'):
        # Include only candidates.
        queryset.filter(role='candidate')
    else:
        # Exclude candidates and party memberships.
        queryset.exclude(role__in=('member', 'candidate'))

    for membership in queryset.prefetch_related('contact_details', 'person', 'person__links', 'person__sources', 'post'):
        person = membership.person

        # Not sure why this is necessary.
        if not isinstance(membership.extras, dict):
            membership.extras = json.loads(membership.extras)
        if not isinstance(person.extras, dict):
            person.extras = json.loads(person.extras)

        try:
            party_name = Membership.objects.select_related('organization').get(organization__classification='party', role='member', person=person).organization.name
        except Membership.DoesNotExist:
            party_name = None

        if person.gender == 'male':
            gender = 'M'
        elif person.gender == 'female':
            gender = 'F'
        else:
            gender = None

        # Candidates only.
        incumbent = person.extras.pop('incumbent', None)

        # @see https://represent.opennorth.ca/api/#fields
        representative = {
            'name': person.name,
            'elected_office': membership.role,
            'party_name': party_name,
            'email': next((contact_detail.value for contact_detail in membership.contact_details.all() if contact_detail.type == 'email'), None),
            'photo_url': person.image or None,
            'personal_url': get_personal_url(person),
            'gender': gender,
            'offices': json.dumps(get_offices(membership)),
            'extra': json.dumps(get_extra(person)),
        }

        sources = list(person.sources.all())

        # The first URL ought to be the most generic source.
        representative['source_url'] = sources[0].url

        if len(sources) > 1:
            # The last URL ought to be the most specific source.
            representative['url'] = sources[-1].url

        if incumbent:
            representative['incumbent'] = True

        match = re.search(r'^(\S+) (Ward \d+)$', membership.post.label)

        # If the person is part of Peel Regional Council.
        if match:
            parent = Division.objects.get(subtype1='csd', subtype2='', name=match.group(1))
            division = Division.objects.get(subtype1='csd', subid1=parent.subid1, name=match.group(2))
            boundary_set_slug = next((k for k, v in settings.IMAGO_BOUNDARY_MAPPINGS.items() if v['prefix'].startswith(parent.id)), None)
            representative['district_name'] = membership.post.label
            representative['boundary_url'] = '/boundaries/{}/ward-{}/'.format(boundary_set_slug, division.subid2)
            representatives.append(representative)

        # If the person is associated to multiple boundaries.
        elif re.search(r'^Wards\b', membership.post.label):
            for district_id in re.findall(r'\d+', membership.post.label):
                representative = representative.copy()
                representative['district_id'] = district_id
                representative['district_name'] = 'Ward {}'.format(district_id)
                representatives.append(representative)

        else:
            division_id = metadata['division_id']

            if re.search('^ocd-division/country:ca/csd:(\d{7})\Z', division_id):
                geographic_code = division_id[-7:]
            elif re.search('^ocd-division/country:ca/cd:(\d{4})\Z', division_id):
                geographic_code = division_id[-4:]
            else:
                geographic_code = None

            post_label = remove_suffix_re.sub('', membership.post.label)

            # If the post label is numeric.
            if re.search(r'^\d+\Z', post_label):
                representative['district_id'] = post_label

            # If the person has a boundary URL.
            elif membership.extras.get('boundary_url'):
                representative['district_name'] = post_label
                representative['boundary_url'] = membership.extras['boundary_url']

            # If the post label is a Census geographic name.
            elif post_label == metadata['division_name'] and geographic_code:
                representative['district_name'] = post_label
                if len(geographic_code) == 7:
                    representative['boundary_url'] = '/boundaries/census-subdivisions/{}/'.format(geographic_code)
                elif len(geographic_code) == 4:
                    representative['boundary_url'] = '/boundaries/census-divisions/{}/'.format(geographic_code)

            else:
                representative['district_name'] = post_label
                district_id = re.search(r'^(?:District|Division|Ward) (\d+)\Z', post_label)
                if district_id:
                    representative['district_id'] = district_id.group(1)

            representatives.append(representative)

    return HttpResponse(json.dumps(representatives), content_type='application/json')


def get_extra(record):
    extra = record.extras
    for link in record.links.all():
        domain = '.'.join(urlsplit(link.url).netloc.split('.')[-2:])
        if domain in ('facebook.com', 'fb.com'):
            extra['facebook'] = link.url
        elif domain == 'instagram.com':
            extra['instagram'] = link.url
        elif domain == 'linkedin.com':
            extra['linkedin'] = link.url
        elif domain == 'twitter.com':
            extra['twitter'] = link.url
        elif domain == 'youtube.com':
            extra['youtube'] = link.url
    return extra
