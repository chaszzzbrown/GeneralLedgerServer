# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Context, Template
from django.template.loader import get_template
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from gldata.models import SessionData

from glservice import TPIUtils

def CorsHttpResponse(response):
    httpResponse = HttpResponse(response)
    httpResponse['Access-Control-Allow-Origin'] = '*'
    httpResponse['Access-Control-Max-Age'] = '120'
    httpResponse['Access-Control-Allow-Credentials'] = 'true'
    httpResponse['Access-Control-Allow-Methods'] = 'HEAD,GET,OPTIONS,POST,DELETE'
    httpResponse['Access-Control-Allow-Headers'] = 'origin,content-type,accept,x-requested-with'
    return httpResponse

@csrf_exempt
def echo_LTI_vars(request):
    s = "<html><body>"
    s += "<h1>Launch Params as a Dict:</h1>"
    s += "<p>{<br/>"
    # s += "<h1>List of POST request params</h1><ul>"
    for k,v in request.POST.items():
        s += "    &quot;"+k+"&quot;:&quot;"+v+"&quot;,<br/>"
    s += "}</p><br/>"
    s+="</body></html>"
    return CorsHttpResponse(s)

@csrf_exempt
def tool_launch(request):
    launch_data = {}
    for k,v in request.POST.items():
        launch_data[k]=v

    if TPIUtils.has_valid_signature(launch_data):
        session = SessionData.getOrCreateSession(launch_data)
        return redirect(settings.APP_REDIRECT_URL+'/#/'+session.session_id+'/')
    else:
        return HttpResponse('Unauthorized', status=401)

@csrf_exempt
def tool_launch_with_outcome(request):
    launch_data = {}
    for k,v in request.POST.items():
        launch_data[k]=v

    if TPIUtils.has_valid_signature(launch_data):
        session = SessionData.getOrCreateSession(launch_data)
        import random
        score = random.uniform(0, 10)
        pnum = launch_data['custom_currentquestion']
        guid = launch_data['custom_target_' + pnum]
        TPIUtils.submit_outcome(launch_data, problemNumber=pnum, problem_guid=guid, score=score, duration=700, submissionCount=1)
        return redirect(settings.APP_REDIRECT_URL+'/#/'+session.session_id+'/')
    else:
        return HttpResponse('Unauthorized', status=401)
