from coffin.shortcuts import render_to_response
from django.template import RequestContext
from reports.models import Report

def home(request):
  return render_to_response('index.html', RequestContext(request, {
    'reports': Report.objects.all(),
  }))
