import json
from django.db import models
from datetime import datetime
from django.utils.timezone import utc
from gldata.grading import grade

# Create your models here.
class SessionData(models.Model):
    
    session_id = models.CharField(max_length=160, unique=True, db_index=True) 
                                        # this is the unique combination of the custom_resource_id and the user_id
    session_creation_date = models.DateTimeField(auto_now_add=True)
    session_launch_date = models.DateTimeField(auto_now=True)
    course_end_date = models.DateTimeField()
    launch_mode = models.CharField(max_length=16)
                                        # this is to prevent overwriting data unless the mode is 'do'
    
    launch_data = models.TextField()    # contains the TPI Launch data for the most recent launch, as a JSON encoded dict
    
    problem_state_data = models.TextField(default="{}")
                                        # contains the most recently saved student data, encoded as JSON
    @classmethod
    def constructSessionID(cls, launch_dict):                                    
        return launch_dict['custom_resource_id']+'__'+launch_dict['user_id']
    
    @classmethod
    def getOrCreateSession(cls, launch_dict):
        session_id = SessionData.constructSessionID(launch_dict)
        
        try:
            session = SessionData.objects.get(session_id=session_id)
            return session
        except SessionData.DoesNotExist:
            return SessionData.createSession(launch_dict)
    
    @classmethod
    def createSession(cls, launch_dict):
        '''
        the launch_dict is the dict of key/value pairs POSTed to us by the TPI launch; some of which we need to keep around
        for use when sending outcomes.
        
        An IntegrityError will be thrown by django if session_id is not not unique.
        '''
        session_id = SessionData.constructSessionID(launch_dict)
        encoded_dict = json.dumps(launch_dict)
        launch_type = launch_dict['custom_mode']
        session = SessionData.objects.create(session_id=session_id,
                                             launch_mode=launch_type,
                                             launch_data=encoded_dict,
                                             course_end_date=datetime.strptime(launch_dict['course_end_date'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=utc))
        return session
    
class ProblemDefinition(models.Model):
    
    problem_guid = models.CharField(max_length=80, unique=True, db_index=True)
    problem_data = models.TextField(default='{}')   #structure defined by gl angular app; this is the problem setup
    correct_data = models.TextField(default='[]')   #array of structures defined by gl angular app; these are the correct journal entries
    
    def grade_response(self, student_answers_json):
        '''
        returns a tuple of valid=True, grade=float in [0,1], correct=list of the index of the student answers which are correct
        or a tuple of valid=False, grade=0, some error message
        '''
        try:
            student_answers = json.loads(student_answers_json)
            assert isinstance(student_answers, list)
        except ValueError:
            return False, 0, 'student_answers is not valid JSON'
        except AssertionError:
            return False, 0, 'student_answers is not a list of objects'

        try:
            correct_answers = json.loads(self.correct_data)
            assert isinstance(student_answers, list)
        except ValueError:
            return False, 0, 'correct_data is not valid JSON for problem_guid:"'+self.problem_guid+'"'
        except AssertionError:
            return False, 0, 'correct_data is not a list of objects for problem_guid:"'+self.problem_guid+'"'
        
        return grade(student_answers, correct_answers)
        
        
        
        
        
    
    