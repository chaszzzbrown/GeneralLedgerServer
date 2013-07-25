from django.conf.urls import patterns, include, url

from django.conf.urls.defaults import *

from gldata.views import *


urlpatterns = patterns('',
    
    # Examples:
    # url(r'^$', 'glservice.views.home', name='home'),
    
    url(r'^get_session_data/(?P<session_id>\w+)/', get_session_data),
    url(r'^put_session_state_data/(?P<session_id>\w+)/', put_session_state_data),

    url(r'^create_problem_definition/(?P<problem_guid>[\w\-]+)/', create_problem_definition),
    url(r'^put_problem_definition/(?P<problem_guid>[\w\-]+)/', put_problem_definition),
    url(r'^put_solution/(?P<problem_guid>[\w\-]+)/', put_solution),
    url(r'^get_problem_definition/(?P<problem_guid>[\w\-]+)/', get_problem_definition),
    url(r'^delete_problem_definition/(?P<problem_guid>[\w\-]+)/', delete_problem_definition),
    
    url(r'^get_problem_list/', get_problem_list),
    url(r'^get_problem/(?P<problem_guid>[\w\-]+)/', get_problem),
    
    
    url(r'^grade_problem/(?P<problem_guid>[\w\-]+)/', grade_problem),
    url(r'^grade_problem_and_report/(?P<session_id>\w+)/(?P<problem_guid>[\w\-]+)/', grade_problem_and_report),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
