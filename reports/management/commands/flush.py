import os
from six.moves.urllib.parse import urlsplit

from django.core.management.base import BaseCommand
from pupa.core import _configure_db, db

from scrapers.tasks import get_definition

class Command(BaseCommand):
  args = '<jurisdiction-id ...>'
  help = 'Deletes all documents from one jurisdiction'

  def handle(self, *args, **options):
    url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')
    parsed = urlsplit(url)
    _configure_db(url, parsed.port, parsed.path[1:])

    for jurisdiction_id in args:
      if db.jurisdictions.find({'_id': jurisdiction_id}).count():
        for membership in db.memberships.find({'jurisdiction_id': jurisdiction_id}):
          db.people.remove({'_id': membership['person_id']})
        db.memberships.remove({'jurisdiction_id': jurisdiction_id})
        db.organizations.remove({'jurisdiction_id': jurisdiction_id})
      else:
        print("Couldn't find jurisdiction_id %s" % jurisdiction_id)
