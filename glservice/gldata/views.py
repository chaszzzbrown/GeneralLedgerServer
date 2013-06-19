from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Context, Template
from django.template.loader import get_template
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db import IntegrityError

from gldata.models import SessionData, ProblemDefinition
import json

def CorsHttpResponse(response, status=200):
    httpResponse = HttpResponse(response)
    httpResponse['Access-Control-Allow-Origin'] = '*'
    httpResponse['Access-Control-Max-Age'] = '120'
    httpResponse['Access-Control-Allow-Credentials'] = 'true'
    httpResponse['Access-Control-Allow-Methods'] = 'HEAD,GET,OPTIONS,POST,DELETE'
    httpResponse['Access-Control-Allow-Headers'] = 'origin,content-type,accept,x-requested-with'
    httpResponse.status_code = status
    return httpResponse

def get_session_data(request, session_id):
    try:
        session = SessionData.objects.get(session_id=session_id)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching session_id for %s"}' % session_id, 404)
        return response
    
    package = {}
    package['session_id'] = session_id
    package['launch_mode'] = session.launch_mode
    try:
        package['launch_data'] = json.loads(session.launch_data)
    except ValueError:
        response = CorsHttpResponse('{"status":"error", "details":"launch_data is not valid JSON"}', 400)

    try:
        package['session_state'] = json.loads(session.problem_state_data)
    except ValueError:
        response = CorsHttpResponse('{"status":"error", "details":"session_state is not valid JSON"}', 400)
    
    return CorsHttpResponse(json.dumps(package))

@csrf_exempt
def put_session_state_data(request, session_id):
    try:
        session = SessionData.objects.get(session_id=session_id)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching session_id for %s"}' % session_id, 404)
        return response
    
    try:
        state_data = json.loads(request.POST['session_state'])
    except ValueError:
        response = CorsHttpResponse('{"status":"error", "details":"session_state is not valid JSON"}', 400)
        return response
    except KeyError:
        response = CorsHttpResponse('{"status":"error", "details":"missing required parameter session_state"}', 400)
        return response
    
    session.problem_state_data = request.POST['session_state']
    session.save()
    
    return CorsHttpResponse('OK')
    
@csrf_exempt
def create_problem_definition(request, problem_guid):
    try:
        problem = ProblemDefinition.objects.create(problem_guid=problem_guid)
    except IntegrityError:
        response = CorsHttpResponse('{"status":"error", "details":"problem_guid %s already exists"}' % problem_guid, 400)
        return response
    
@csrf_exempt
def put_problem_definition(request, problem_guid):
    
    problem, created = ProblemDefinition.objects.get_or_create(problem_guid=problem_guid)
    
    try:
        problem.problem_data = request.POST['problem_data']
    except KeyError:
        pass

    try:
        problem.correct_data = request.POST['correct_data']
    except KeyError:
        pass
    
    problem.save()
    
    return CorsHttpResponse('OK')
    

def get_problem_definition(request, problem_guid):
    try:
        problem = ProblemDefinition.objects.get(problem_guid=problem_guid)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching problem_guid for %s"}' % problem_guid, 404)
        return response
    
    
    return CorsHttpResponse('{"problem_data":"'+problem.problem_data+'",',
                            '"correct_data":"'+problem.correct_data+'"}')
    
def get_problem(request, problem_guid):
    try:
        problem = ProblemDefinition.objects.get(problem_guid=problem_guid)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching problem_guid for %s"}' % problem_guid, 404)
        return response
    
    return CorsHttpResponse(problem.problem_data)
    
@csrf_exempt
def grade_problem_and_report(request, session_id, problem_guid):
    # ToDo - report result
    return grade_problem(request, problem_guid)

@csrf_exempt
def grade_problem(request, problem_guid):
    try:
        problem = ProblemDefinition.objects.get(problem_guid=problem_guid)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching problem_guid for %s"}' % problem_guid, 404)
        return response

    try:
        student_data = request.POST['student_data']
    except KeyError:
        return CorsHttpResponse('{"status":"error", "details":"missing required parameter student_data"}', 400)
    
    valid, result = problem.grade_response(student_data)
    
    return CorsHttpResponse(result, 200 if valid else 400)
    
