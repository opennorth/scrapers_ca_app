from django.core.management.base import BaseCommand
from opencivicdata.models import Jurisdiction, Person

class Command(BaseCommand):
  args = '<jurisdiction-id ...>'
  help = 'Deletes all documents from one jurisdiction'

  def handle(self, *args, **options):
    for jurisdiction_id in args:
      try:
        Person.objects.filter(memberships__organization__jurisdiction_id=jurisdiction_id).delete()
        Jurisdiction.objects.filter(id=jurisdiction_id}).delete()  # cascades everything except Person and Division
      except Jurisdiction.DoesNotExist:
        print("No Jurisdiction with id='%s'" % jurisdiction_id)
