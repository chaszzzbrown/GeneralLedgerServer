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
    s += "<h1>List of POST request params</h1><ul>"
    for k,v in request.POST.items():
        s += "<li>"+k+":"+v+"</li>"
    s += "</ul>"
    s += "<h1>List of GET request params</h1><ul>"
    for k,v in request.GET.items():
        s += "<li>"+k+":"+v+"<//li>"
    s += "</ul>"
    s+="</body></html>"
    return HttpResponse(s)