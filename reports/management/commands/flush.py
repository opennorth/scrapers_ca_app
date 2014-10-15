from django.core.management.base import BaseCommand

from scrapers.tasks import get_definition

class Command(BaseCommand):
  args = '<division-id ...>'
  help = 'Deletes all documents from one jurisdiction'

  def handle(self, *args, **options):
    for division_id in args:
      if db.jurisdictions.find({'_id': jurisdiction_id}).count():
        for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id}):
          db.people.remove({'_id': membership['person_id']})
        db.memberships.remove({'jurisdiction_id': jurisdiction_id})
        db.organizations.remove({'jurisdiction_id': jurisdiction_id})
      else:
        print("Couldn't find jurisdiction_id %s" % jurisdiction_id)
