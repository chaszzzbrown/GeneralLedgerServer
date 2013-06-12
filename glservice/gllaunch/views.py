# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Context, Template
from django.template.loader import get_template
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def echo_LTI_vars(request):
    s = "<html><body>"
    s += "<h1>List of request params</h1>"
    for k,v in request.REQUEST.items():
        s += "<p>"+k+":"+v+"</p>"
    s+="</body></html>"
    return HttpResponse(s)