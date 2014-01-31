import importlib
import json
import os
import os.path
import sys

import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapers_ca_app.settings")
sys.path.append(os.path.abspath('scrapers'))

from reports.models import Report

data = json.loads(requests.get('http://represent.opennorth.ca/representative-sets/?limit=0').content)
names = {}
for obj in data['objects']:
  names[obj['name']] = obj['data_url']

for module_name in os.listdir('scrapers'):
  if os.path.isdir(os.path.join('scrapers', module_name)) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
      jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
      if jurisdiction_id:  # We've found the module.
        name = getattr(obj, 'name', None)
        if name:
          if name in names:
            obj = Report.objects.get(module=module_name)
            if not obj.exception and not names[name].startswith('http://scrapers.herokuapp.com/represent/'):
              print 'Replace %s\n  http://scrapers.herokuapp.com/represent/%s/\n' % (name, module_name)
          else:
            obj = Report.objects.get(module=module_name)
            if not obj.exception:
              print 'Import %s\n  http://scrapers.herokuapp.com/represent/%s/\n' % (name, module_name)
        else:
          print 'No name for %s' % module_name
