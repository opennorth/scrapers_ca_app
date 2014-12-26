from django.core.management.base import BaseCommand
from opencivicdata.models import Jurisdiction, Person


class Command(BaseCommand):
    args = '<division-id ...>'
    help = 'Deletes all documents from one jurisdiction'

    def handle(self, *args, **options):
        for division_id in args:
            try:
                jurisdiction_id = '{}/{}'.format(division_id.replace('ocd-division', 'ocd-jurisdiction'), 'legislature')
                qs = Person.objects.filter(memberships__organization__jurisdiction_id=jurisdiction_id)
                people_count = qs.count()
                qs.delete()
                qs = Jurisdiction.objects.filter(id=jurisdiction_id)
                jurisdiction_count = qs.count()
                qs.delete()  # cascades everything except Person and Division
                print("%s: %s people in %s jurisdiction" % (jurisdiction_id, people_count, jurisdiction_count))
            except Jurisdiction.DoesNotExist:
                print("No Jurisdiction with id='%s'" % jurisdiction_id)
