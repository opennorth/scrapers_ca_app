import logging
from collections import Counter

from django.db.models import Count
from django.core.management.base import BaseCommand
from opencivicdata.models import Membership, Organization, Person, Post, MembershipContactDetail
from opencivicdata.models.jurisdiction import Jurisdiction

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<division-id>'
    help = 'Checks the consistency of the database'

    def handle(self, *args, **options):
        empty_organizations = {'Parliament of Canada', 'Senate'}

        if args:
            division_id = args[0]
            jurisdictions = Jurisdiction.objects.filter(division_id=division_id)
            organizations = Organization.objects.filter(jurisdiction__in=jurisdictions)
            posts = Post.objects.filter(organization__in=organizations)
            people = Person.objects.filter(memberships__organization__in=organizations)
            memberships = Membership.objects.filter(person__id__in=people)
            contact_details = MembershipContactDetail.objects.filter(membership__in=memberships)
        else:
            jurisdictions = Jurisdiction.objects
            organizations = Organization.objects
            posts = Post.objects
            people = Person.objects
            memberships = Membership.objects
            contact_details = MembershipContactDetail.objects

        post_memberships_count = posts.values('id').annotate(count=Count('memberships'))

        # Validate the number of organizations per jurisdiction.
        results = jurisdictions.values('id').annotate(count=Count('organizations')).exclude(count=1)
        if len(results) > 1 or results and results[0] != {'count': 3, 'id': 'ocd-jurisdiction/country:ca/legislature'}:
            log.error('%d jurisdictions do not have one organization' % len(results))
            for result in results:
                log.info('%d %s' % (result['count'], result['id']))

        # Validate the presence of posts and memberships on organizations.
        results = set(organizations.values('id').exclude(classification='party').annotate(count=Count('posts')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('non-party organizations have no posts', results)
        results = set(organizations.values('id').annotate(count=Count('memberships')).filter(count=0).values_list('name', flat=True)) - empty_organizations
        self.report_value('organizations have no memberships', results)

        # Validate the number of memberships per post.
        results = Counter(post_memberships_count.filter(count=0).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with no memberships', results)
        results = Counter(post_memberships_count.filter(count__gt=1).values_list('organization__name', flat=True))
        self.report_count('organizations have posts with many memberships', results)

        # Validate the presence of posts on memberships.
        results = Counter(memberships.filter(post_id=None).exclude(organization__classification='party').values_list('organization__name', flat=True))
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
        results = self.repeated(contact_details.filter(type='email').values_list('value', flat=True))
        self.report_count('membership contact details with the same email', results)

        # Validate presence of email contact detail.
        jurisdiction_with_no_email = [
            # Javascript-encoded email
            'ocd-jurisdiction/country:ca/csd:1217030/legislature',  # Cape Breton
            # Webform email
            'ocd-jurisdiction/country:ca/csd:1310032/legislature',  # Fredericton
            'ocd-jurisdiction/country:ca/csd:2423027/legislature',  # Québec
            'ocd-jurisdiction/country:ca/csd:2464008/legislature',  # Terrebonne
            'ocd-jurisdiction/country:ca/csd:2466097/legislature',  # Pointe-Claire
            'ocd-jurisdiction/country:ca/csd:3530016/legislature',  # Waterloo
            'ocd-jurisdiction/country:ca/csd:3530035/legislature',  # Woolwich
            'ocd-jurisdiction/country:ca/csd:4706027/legislature',  # Regina
            'ocd-jurisdiction/country:ca/csd:4806016/legislature',  # Calgary
        ]
        leaders_with_no_email = [
            'ocd-jurisdiction/country:ca/cd:3521/legislature',  # Peel
            'ocd-jurisdiction/country:ca/csd:2437067/legislature',  # Trois-Rivières
            'ocd-jurisdiction/country:ca/csd:2456083/legislature',  # Saint-Jean-sur-Richelieu
            'ocd-jurisdiction/country:ca/csd:2494068/legislature',  # Saguenay
            'ocd-jurisdiction/country:ca/csd:3520005/legislature',  # Toronto
            'ocd-jurisdiction/country:ca/csd:3521024/legislature',  # Caledon
            'ocd-jurisdiction/country:ca/csd:3530013/legislature',  # Kitchener
            'ocd-jurisdiction/country:ca/csd:4711066/legislature',  # Saskatoon
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
                    log.error('%2d memberships have no email in %s' % (memberships_with_no_email, organization.name))

    def repeated(self, results):
        return {value: count for value, count in Counter(results).items() if count > 1}

    def report_value(self, message, results):
        if results:
            log.error('%d %s:' % (len(results), message))
            for value in results:
                log.info(value)
            log.info('---')

    def report_count(self, message, results):
        if results:
            log.error('%d %s:' % (len(results), message))
            for value, count in results.items():
                log.info('%d %s' % (count, value))
            log.info('---')
