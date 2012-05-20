from django.template import Context,loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ad.models import *

@login_required
def home(request):
    t = loader.get_template('ad/index.html')
    c = Context ({})
    return HttpResponse(t.render(c))
