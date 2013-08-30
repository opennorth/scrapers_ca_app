from django.http import HttpResponse
from django.template import Template, Context
from mycityhall_scrapers import export_represent
import zipfile
import os, sys
import StringIO

def home(request):
  scrapers = [{'name':'montreal', 'status':'working'}, {'name':'outremont', 'status': 'not working'}]
  row = "<tr><td>{{ name }}</td><td>{{ status }}</td></tr>"


  row = Template("<tr><td>{{ name }}</td><td>{{ status }}</td></tr>")

  raw_template = "<table>" 
  for scraper in scrapers:
      raw_template = raw_template + row.render(Context({'name':scraper['name'], 'status':scraper['status']}))

  raw_template = raw_template+ "</table>"
  return HttpResponse(raw_template)

def represent_json(request):
  os.system('rm -rf mycityhall_scrapers/represent_data/*')
  export_represent.main()
  # Files (local path) to put in the .zip
   # FIXME: Change this (get paths from DB etc)
  filenames = os.listdir('mycityhall_scrapers/represent_data/')

   # Folder name in ZIP archive which contains the above files
   # E.g [thearchive.zip]/somefiles/file2.txt
   # FIXME: Set this to something better
  zip_subdir = "mycityhall_scrapers/represent_data"
  zip_filename = "%s.zip" % zip_subdir

   # # Open StringIO to grab in-memory ZIP contents
  s = StringIO.StringIO()

   # # The zip compressor
  zf = zipfile.ZipFile(s, "w")

  for fpath in filenames:
   #     # Calculate path for file in zip
    fdir, fname = os.path.split(fpath)
    zip_path = os.path.join(zip_subdir, fname)

   #     # Add file, at correct path
  # print fpath
    zf.write('mycityhall_scrapers/represent_data/'+fpath, zip_path)

   # # Must close zip for all contents to be written
  zf.close()

   # # Grab ZIP file from in-memory, make response with correct MIME-type
  resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
   # # ..and correct content-disposition
  resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

  return resp
