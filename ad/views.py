from ad.models import *
from ad.forms import *
from ad.geocode import handle_uploaded_file

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context,loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ad.models import *


@login_required
def home(request):
    # Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            contents = handle_uploaded_file(newdoc.docfile, request.POST.getlist('district'))

            # Load list of documents in cache dir
            documents = Document.objects.all()

            # Render home page with the documents, form, requested districts
            return render_to_response(
                'ad/index.html',
                {'documents': documents, 'form': form, 'districts_requested': request.POST.getlist('district'), 'contents': contents},
                context_instance=RequestContext(request)
            )

        # Bounce back to home page if file not included
        else:
            return HttpResponseRedirect(reverse('ad.views.home'))
           
    #Load homepage (request.method = 'GET')
    else:
        # A empty unbound form
        form = DocumentForm() 
            
        # Load list of documents in cache dir
        documents = Document.objects.all()
    
        # Render home page with the documents and the form
        return render_to_response(
        'ad/index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
