from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render_to_response
from .models import Report
import csv
def home(request):
  scrapers = Report.objects.all()
  row = "<tr><td>{{ name }}</td><td>{{ status }}</td></tr>"


  row = Template("<tr><td>{{ name }}</td><td>{{ status }}</td><td>{{ note }}</td></tr>")

  raw_template = "<table>" 
  for scraper in scrapers:
      raw_template = raw_template + row.render(Context({'name':scraper.name , 'status':scraper.status, 'note':scraper.error}))

  raw_template = raw_template+ "</table>"
  return HttpResponse(raw_template)

def serve_csv(request):
  
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="scraperreport.csv"'

  writer = csv.writer(response)
  writer.writerow(['Scraper', 'Status', 'Error'])

  scrapers = Report.objects.all()
  for scraper in scrapers:
    row = [scraper.name, scraper.status, scraper.error]
    writer.writerow(row)
  return response