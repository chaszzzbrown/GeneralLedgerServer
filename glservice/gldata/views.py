from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Context, Template
from django.template.loader import get_template
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db import IntegrityError

from gldata.models import SessionData, ProblemDefinition
from glservice import TPIUtils
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
        json.loads(request.body)
    except ValueError:
        response = CorsHttpResponse('{"status":"error", "details":"session_state is not valid JSON"}', 400)
        return response
    
    session.problem_state_data = request.body
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
    try:
        session = SessionData.objects.get(session_id=session_id)
        launch_data = json.loads(session.launch_data)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching session_id for %s"}' % session_id, 404)
        return response
    except ValueError:
        response = CorsHttpResponse('{"status":"error", "details":"launch_data is not valid JSON"}', 400)
        return response

    try:
        problem = ProblemDefinition.objects.get(problem_guid=problem_guid)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching problem_guid for %s"}' % problem_guid, 404)
        return response

    student_data = request.body

    try:
        result = problem.grade_response(student_data)
    except Exception as e:
        return CorsHttpResponse(str(e), 400)

    if session.launch_mode == 'do':
        try:
            pnum, points = session.problem_assignment_info(problem_guid)
        except TypeError:
            return CorsHttpResponse('Points not found for problem guid ' + problem_guid, 400)

        score = float(result['score']) * points

        # TODO: duration, submissionCountkk
        TPIUtils.submit_outcome(launch_data, problem_guid=problem_guid, score=score, duration=700, submissionCount=1)
    # TODO: test if submission was successful
    return CorsHttpResponse(json.dumps(result), 200)


@csrf_exempt
def grade_problem(request, problem_guid):
    try:
        problem = ProblemDefinition.objects.get(problem_guid=problem_guid)
    except SessionData.DoesNotExist:
        response = CorsHttpResponse('{"status":"error", "details":"no matching problem_guid for %s"}' % problem_guid, 404)
        return response

    student_data = request.body

    try:
        result = problem.grade_response(student_data)
    except Exception as e:
        return CorsHttpResponse(str(e), 400)

    return CorsHttpResponse(json.dumps(result), 200)
