
from ad.models import *
from ad.forms import *
from ad.geocode import handle_uploaded_file

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
=======
from django.template import Context,loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ad.models import *


@login_required
def home(request):
    #Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            #contents = handle_uploaded_file(newdoc)
            #Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('ad.views.list'))
            return HttpResponseRedirect(reverse('ad.views.home'),{'contents': contents})
    else:
    #Load homepage (request.method = 'GET')
        form = DocumentForm() # A empty unbound form
            
    #Load list of documents in cache dir
    documents = Document.objects.all()
    
    # Render home page with the documents and the form
    return render_to_response(
        'ad/index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
