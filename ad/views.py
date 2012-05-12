from django.template import Context,loader
from ad.models import *
from django.http import HttpResponse

def home(request):
    t = loader.get_template('ad/index.html')
    c = Context ({})
    return HttpResponse(t.render(c))
