from django.http import HttpResponse
from django.template import Template, Context

def home(request):
  scrapers = [{'name':'montreal', 'status':'working'}, {'name':'outremont', 'status': 'not working'}]
  row = "<tr><td>{{ name }}</td><td>{{ status }}</td></tr>"


  row = Template("<tr><td>{{ name }}</td><td>{{ status }}</td></tr>")

  raw_template = "<table>" 
  for scraper in scrapers:
      raw_template = raw_template + row.render(Context({'name':scraper['name'], 'status':scraper['status']}))

  raw_template = raw_template+ "</table>"
  return HttpResponse(raw_template)