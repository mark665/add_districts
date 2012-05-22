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


@login_required
def home(request):
    # Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Address_List(user=request.user, address_list = request.FILES['docfile'])
            newdoc.save()

            districts_requested = request.POST.getlist('district')

            result_file = handle_uploaded_file(newdoc.address_list, districts_requested)

            # Load list of documents in cache dir
            documents = Address_List.objects.filter(user_id=request.user.id)

            # Render home page with the documents, form, requested districts
            return render_to_response(
                'ad/index.html',
                {'documents': documents, 'form': form, 'districts_requested': request.POST.getlist('district'), 'contents': result_file},
                context_instance=RequestContext(request)
            )

        # Bounce back to home page if file not included
        else:
            return HttpResponseRedirect(reverse('ad.views.home'))
           
    #Load homepage (request.method = 'GET')
    else:
        # A empty unbound form
        form = DocumentForm() 
            
        #Load list of documents in cache dir
        documents = Address_List.objects.filter(user_id=request.user.id)

        # Render home page with the documents and the form
        return render_to_response(
        'ad/index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    	)
