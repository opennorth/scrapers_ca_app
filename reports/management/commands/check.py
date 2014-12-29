import logging
from collections import Counter

from django.db.models import Count
from django.core.management.base import BaseCommand
from opencivicdata.models import Membership, Organization, Person, Post, MembershipContactDetail
from opencivicdata.models.jurisdiction import Jurisdiction

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<division-id ...>'
    help = 'Checks the consistency of the database'

    def handle(self, *args, **options):
        empty_organizations = {'Parliament of Canada', 'Senate'}
        organizations = Organization.objects.values('id')
        people = Person.objects
        post_memberships_count = Post.objects.values('id').annotate(count=Count('memberships'))

        # Validate the number of organizations per jurisdiction.
        results = Jurisdiction.objects.values('id').annotate(count=Count('organizations')).exclude(count=1)
        if len(results) > 1 or results[0] != {'count': 3, 'id': 'ocd-jurisdiction/country:ca/legislature'}:
            log.error('%d jurisdictions do not have one organization' % len(results))
            for result in results:
                log.info('%d %s' % (result['count'], result['id']))

        # Validate the presence of posts and memberships on organizations.
        results = set(organizations.exclude(classification='party').annotate(count=Count('posts')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('non-party organizations have no posts', results)
        results = set(organizations.annotate(count=Count('memberships')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('organizations have no memberships', results)

        # Validate the number of memberships per post.
        results = Counter(post_memberships_count.filter(count=0).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with no memberships', results)
        results = Counter(post_memberships_count.filter(count__gt=1).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with many memberships', results)

        # Validate the presence of posts on memberships.
        results = Counter(Membership.objects.filter(post_id=None).exclude(organization__classification='party').values_list('organization__name', flat=True))
        self.report_count('non-party organizations have memberships with no posts', results)

        # Validate that people have at most one post-membership and one party-membership.
        results = people.values('id').exclude(memberships__organization__classification='party').annotate(count=Count('memberships')).exclude(count=1).values_list('name', flat=True)
        self.report_value('people have many non-party memberships', results)
        results = people.values('id').filter(memberships__organization__classification='party').annotate(count=Count('memberships')).exclude(count=1).values_list('name', flat=True)
        self.report_value('people have many party memberships', results)

        # Validate the uniqueness of names, images and link URLs.
        results = self.repeated(people.exclude(image='').values_list('image', flat=True))
        self.report_count('people have the same image', results)
        results = self.repeated(people.values_list('name', flat=True))
        self.report_count('people have the same name', results)
        results = self.repeated(people.exclude(links__url=None).values_list('links__url', flat=True))
        self.report_count('people have the same link URL', results)

        # Validate the uniqueness of email contact detail values.
        results = self.repeated(MembershipContactDetail.objects.filter(type='email').values_list('value', flat=True))
        self.report_count('membership contact details with the same email', results)

    def repeated(self, results):
        return {value: count for value, count in Counter(results).items() if count > 1}

    def report_value(self, message, results):
        if results:
            log.error('%d %s' % (len(results), message))
            for value in results:
                log.info(value)

    def report_count(self, message, results):
        if results:
            log.error('%d %s' % (len(results), message))
            for value, count in results.items():
                log.info('%d %s' % (count, value))
            log.info('---')
