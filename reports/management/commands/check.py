import logging
import operator
import os
import sys
from collections import Counter

from django.db.models import Count
from django.core.management.base import BaseCommand
from opencivicdata.models import Membership, Organization, Person, Post, MembershipContactDetail
from opencivicdata.models.jurisdiction import Jurisdiction

from reports.utils import module_name_to_metadata

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Checks the consistency of documents per jurisdiction'

    def add_arguments(self, parser):
        parser.add_argument('module', nargs='?')

    def handle(self, *args, **options):
        sys.path.append(os.path.abspath('scrapers'))

        empty_organizations = {'Parliament of Canada', 'Senate'}

        if options['module']:
            division_id = module_name_to_metadata(options['module'])['division_id']
            jurisdictions = Jurisdiction.objects.filter(division_id=division_id)
        else:
            # Exclude candidate scrapers.
            jurisdictions = Jurisdiction.objects.exclude(classification='executive')

        organizations = Organization.objects.filter(jurisdiction__in=jurisdictions)
        posts = Post.objects.filter(organization__in=organizations)
        people = Person.objects.filter(memberships__organization__in=organizations)
        memberships = Membership.objects.filter(person_id__in=people)
        contact_details = MembershipContactDetail.objects.filter(membership__in=memberships)

        # A person has multiple memberships.
        jurisdiction_with_repetition = {
            'ocd-jurisdiction/country:ca/cd:3521/legislature': 4,  # Peel, due to Brampton
            'ocd-jurisdiction/country:ca/csd:3521010/legislature': 4,  # Brampton
        }

        post_memberships_count = posts.values('id').annotate(count=Count('memberships'))

        # Validate the number of organizations per jurisdiction.
        results = jurisdictions.values('id').annotate(count=Count('organizations')).exclude(count=1)
        # The Parliament of Canada has three organizations.
        if len(results) > 1 or results and results[0] != {'count': 3, 'id': 'ocd-jurisdiction/country:ca/legislature'}:
            log.error('{} jurisdictions do not have one organization'.format(len(results)))
            for result in results:
                log.info('{} {}'.format(result['count'], result['id']))

        # Validate the presence of posts and memberships on organizations.
        results = set(organizations.values('id').exclude(classification__in=('committee', 'party')).annotate(count=Count('posts')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('non-committee, non-party organizations have no posts', results)
        results = set(organizations.values('id').exclude(classification='committee').annotate(count=Count('memberships')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('non-committee organizations have no memberships', results)

        # Validate the number of memberships per post.
        results = Counter(post_memberships_count.filter(count=0).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with no memberships (seats may be vacant)', results)
        results = Counter(post_memberships_count.filter(count__gt=1).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with many memberships', results)

        # Validate the presence of posts on memberships.
        results = Counter(memberships.filter(post_id=None).exclude(organization__classification='party').values_list('organization__name', flat=True))
        self.report_count('non-party organizations have memberships with no posts', results)

        # Validate that people have at most one post-membership.
        results = people.values('id').exclude(memberships__organization__classification='party').exclude(memberships__organization__jurisdiction_id__in=jurisdiction_with_repetition.keys()).annotate(count=Count('memberships')).exclude(count=1).values_list('name', flat=True)
        self.report_value('people have many non-party memberships', results)
        for jurisdiction_id, threshold in jurisdiction_with_repetition.items():
            results = people.values('id').exclude(memberships__organization__classification='party').filter(memberships__organization__jurisdiction_id=jurisdiction_id).annotate(count=Count('memberships')).exclude(count__lte=threshold).values_list('name', flat=True)
            self.report_value('people have many non-party memberships in {}'.format(jurisdiction_id), results)

        # Validate that people have at most one party-membership.
        results = people.values('id').filter(memberships__organization__classification='party').annotate(count=Count('memberships')).exclude(count=1).values_list('name', flat=True)
        self.report_value('people have many party memberships', results)

        # Validate the uniqueness of names and images.
        people_without_repetition = people.exclude(memberships__organization__jurisdiction_id__in=jurisdiction_with_repetition.keys())
        results = self.repeated(people_without_repetition.values_list('name', flat=True))
        self.report_count('names are repeated across people', results)
        results = self.repeated(people_without_repetition.exclude(image='').values_list('image', flat=True))
        self.report_count('images are repeated across people', results)
        for jurisdiction_id, threshold in jurisdiction_with_repetition.items():
            people_with_repetition = people.filter(memberships__organization__jurisdiction_id=jurisdiction_id)
            results = self.repeated(people_with_repetition.values_list('name', flat=True), threshold=threshold)
            self.report_count('names are repeated across people in {}'.format(jurisdiction_id), results)
            results = self.repeated(people_with_repetition.exclude(image='').values_list('image', flat=True), threshold=threshold)
            self.report_count('images are repeated across people in {}'.format(jurisdiction_id), results)

        # Validate the uniqueness of link URLs.
        results = self.repeated(people.exclude(links__url=None).values_list('links__url', flat=True))
        self.report_count('link URLs are repeated across people', results)

        # Validate the uniqueness of email contact detail values.
        results = self.repeated(contact_details.filter(type='email').exclude(membership__organization__jurisdiction_id__in=jurisdiction_with_repetition.keys()).values_list('value', flat=True))
        self.report_count('emails are repeated across membership contact details', results)
        for jurisdiction_id, threshold in jurisdiction_with_repetition.items():
            results = self.repeated(contact_details.filter(type='email').filter(membership__organization__jurisdiction_id=jurisdiction_id).values_list('value', flat=True), threshold=threshold)
            self.report_count('emails are repeated across membership contact details in {}'.format(jurisdiction_id), results)

        # Validate presence of email contact detail.
        jurisdiction_with_no_email = [
            # Javascript-encoded email
            'ocd-jurisdiction/country:ca/csd:1217030/legislature',  # Cape Breton
            # Webform email
            'ocd-jurisdiction/country:ca/csd:2423027/legislature',  # Québec
            'ocd-jurisdiction/country:ca/csd:2464008/legislature',  # Terrebonne
            'ocd-jurisdiction/country:ca/csd:3524009/legislature',  # Milton
            'ocd-jurisdiction/country:ca/csd:3530016/legislature',  # Waterloo
            'ocd-jurisdiction/country:ca/csd:3530027/legislature',  # Wellesley
            'ocd-jurisdiction/country:ca/csd:3530035/legislature',  # Woolwich
            'ocd-jurisdiction/country:ca/csd:4706027/legislature',  # Regina
            'ocd-jurisdiction/country:ca/csd:4711066/legislature',  # Saskatoon
            'ocd-jurisdiction/country:ca/csd:4806016/legislature',  # Calgary
            'ocd-jurisdiction/country:ca/csd:5909052/legislature',  # Abbotsford
        ]
        leaders_with_no_email = [
            'ocd-jurisdiction/country:ca/cd:3521/legislature',  # Peel
            'ocd-jurisdiction/country:ca/csd:2437067/legislature',  # Trois-Rivières
            'ocd-jurisdiction/country:ca/csd:2456083/legislature',  # Saint-Jean-sur-Richelieu
            'ocd-jurisdiction/country:ca/csd:2494068/legislature',  # Saguenay
            'ocd-jurisdiction/country:ca/csd:3520005/legislature',  # Toronto
            'ocd-jurisdiction/country:ca/csd:3521024/legislature',  # Caledon
            'ocd-jurisdiction/country:ca/csd:3530013/legislature',  # Kitchener
            'ocd-jurisdiction/country:ca/csd:4811061/legislature',  # Edmonton
            'ocd-jurisdiction/country:ca/csd:4816037/legislature',  # Wood Buffalo
            'ocd-jurisdiction/country:ca/csd:5909052/legislature',  # Abbotsford
            'ocd-jurisdiction/country:ca/csd:5915004/legislature',  # Surrey
        ]
        jurisdiction_ids = jurisdictions.exclude(id__in=jurisdiction_with_no_email).values_list('id', flat=True)
        for jurisdiction_id in jurisdiction_ids:
            for organization in organizations.filter(jurisdiction_id=jurisdiction_id):
                # It's ridiculous that Django can't do a LEFT OUTER JOIN with a WHERE clause.
                memberships_with_no_email = sum(not membership.contact_details.filter(type='email').count() for membership in organization.memberships.all())
                if memberships_with_no_email > 1 or memberships_with_no_email and jurisdiction_id not in leaders_with_no_email:
                    log.error('{:2} memberships have no email in {}'.format(memberships_with_no_email, organization.name))

    def repeated(self, results, *, threshold=1):
        return {value: count for value, count in Counter(results).items() if count > threshold}

    def report_value(self, message, results):
        if results:
            log.error('{} {}:'.format(len(results), message))
            for value in results:
                log.info(value)
            log.info('---')

    def report_count(self, message, results):
        if results:
            log.error('{} {}:'.format(len(results), message))
            for value, count in sorted(results.items(), key=operator.itemgetter(1), reverse=True):
                log.info('{:2} {}'.format(count, value))
            log.info('---')
