"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import IntegrityError
from gldata.models import *
import json

TPI_DICT = {'custom_resource_id':'abcd-efghi', 'user_id':'ABCDEFG-HIJK', 'custom_mode':'do', 'course_end_date':'2013-11-01T17:34:56'}
class SessionDataTestCase(TestCase):
    def setUp(self):
        session = SessionData.createSession(TPI_DICT)
    
    def testUnqique(self):
        '''test uniqueness'''
        self.assertRaises(IntegrityError, SessionData.createSession, TPI_DICT)   
