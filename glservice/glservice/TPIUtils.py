'''
Created on Jun 12, 2013

@author: charlieb
'''

import datetime
import uuid
import cgi
from string import Template

# for testing; example TPI launch data...
TEST_TPI_PARAMS = {
        'context_id': 'urn:udson:pearson.com/xl/devdb:course/138261',
        'context_type': 'CourseSection',
        'custom_assignmenttitle': 'GLv2 Homework 6-25',
        'custom_attemptsallowed': '0',
        'custom_course_id': 'urn:udson:pearson.com/xl/devdb:course/138261_xlnoedx_devdb',
        'custom_courseenddate': '2013-09-22T00:00:00Z',
        'custom_currentquestion': '1',
        'custom_dateavailable': '2013-06-25T00:00:00Z',
        'custom_displaycourseid': '02Y1OL501Y2QD0',
        'custom_firstname': 'GL',
        'custom_handler_urn': 'pearson/xlnoedx_phgl2/slink/x-pearson-xlnoedx_phgl2',
        'custom_institutionId': 'devdb',
        'custom_lastname': 'Tester',
        'custom_membershipslastupdated': '2013-01-22T18:09:22.893Z',
        'custom_mode': 'do',
        'custom_originating_partner': 'xl',
        'custom_partialcredit': '1',
        'custom_partnerId': 'xlnoedx',
        'custom_person_id': 'gl-instructor',
        'custom_points_1': '1',
        'custom_points_2': '1',
        'custom_points_3': '1',
        'custom_print': '1',
        'custom_questiontitle_1': 'glv2-question1 (dev)',
        'custom_questiontitle_2': 'glv2-question2 (dev)',
        'custom_questiontitle_3': 'glv2-question3 (dev)',
        'custom_resource_id': 'urn:udson:pearson.com/xl/devdb:homework/2089614',
        'custom_resultid': 'urn:udson:pearson.com/xl/devdb:partnerhomeworkresult/46581',
        'custom_resultid_role': '$resultidrole',
        'custom_savevalues': '1',
        'custom_target_1': 'GL0001',
        'custom_target_2': 'GL0002',
        'custom_target_3': 'GL0003',
        'custom_tool_proxy_guid': 'd5bfe447-e208-43b5-b2fb-d2a0e1c3b3ad',
        'custom_totalpoints': '3',
        'lti_message_type': 'basic-lti-launch-request',
        'lti_version': 'LTI-1p0',
        'oauth_consumer_key': 'TPI',
        'oauth_nonce': '-4293185738320548860',
        'oauth_signature': 'Eikl+XBdJ3Xsz1/YfIW4OEUPWtQ=',
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': '1372173163',
        'oauth_version': '1.0',
        'resource_link_id': 'UNKNOWN',
        'roles': 'Educator',
        'tool_consumer_instance_guid': 'TPI',
        'user_id': 'urn:udson:pearson.com/xl/devdb:user/35870',
    }

TEST_EXTRA_PARAMS = {
    'transactionId': uuid.uuid4(),
    'timeStamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
    'custom_originating_parner': 'GL',
    'score': 7,
    'problem_guid': 'GL0001',
    'problemNumber': 1,
    'duration': 700,
    'submissionCount': 1
}

WRAPPER_TEMPLATE = '''
<tos:outcomeMessage xsi:schemaLocation="http://www.pearson.com/xsd/tpiOutcomesService_v1p0 tpiOutcomesService_v1p0.xsd" xsi:type="tos:OutcomeMessage.Type" xmlns:cor="http://www.imsglobal.org/services/lti/xsd/CoreOutcomesService_bv1p0" xmlns:tos="http://www.pearson.com/xsd/tpiOutcomesService_v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <tos:messageInfo>
      <tos:dataSource>${custom_tool_proxy_guid}</tos:dataSource>
      <tos:dataSourceName>${custom_originating_partner}</tos:dataSourceName>
      <tos:transactionId>${transactionId}</tos:transactionId>
      <tos:timestamp>$timeStamp</tos:timestamp>
      <tos:partnerId>${custom_partnerId}</tos:partnerId>
      <tos:institutionId>${custom_institutionId}</tos:institutionId>
      <tos:contextIdentifier>$context_id</tos:contextIdentifier>
   </tos:messageInfo>
   $messageBody
</tos:outcomeMessage>
'''

REPLACE_RESULT_TEMPLATE = '''
   <cor:replaceResultRequest>
      <cor:sourcedId>${custom_resultid}</cor:sourcedId>
      <cor:resultRecord>
         <cor:sourcedId>${custom_resultid}</cor:sourcedId>
         <cor:result>
            <cor:statusofResult>
               <cor:displayName>Quiz</cor:displayName>
            </cor:statusofResult>
            <cor:personSourcedId>${user_id}</cor:personSourcedId>
            <cor:lineItemSourcedId>${custom_resource_id}</cor:lineItemSourcedId>
            <cor:date>${timeStamp}</cor:date>
            <cor:resultScore>
               <cor:language>en-US</cor:language>
               <cor:textString>${score}</cor:textString>
            </cor:resultScore>
            <cor:dataSource>${custom_tool_proxy_guid}</cor:dataSource>
            <cor:extension>
                <cor:extensionField>
                    <cor:fieldName>resultDetail</cor:fieldName>
                    <cor:fieldType>any</cor:fieldType>
                    <cor:fieldValue>${extensionBody}</cor:fieldValue>
                </cor:extensionField>
                <cor:extensionField>
                    <cor:fieldName>messageDate</cor:fieldName>
                    <cor:fieldType>any</cor:fieldType>
                    <cor:fieldValue>$timeStamp</cor:fieldValue>
                </cor:extensionField>
            </cor:extension>
         </cor:result>
      </cor:resultRecord>
   </cor:replaceResultRequest>
'''

SIMPLE_ITEM_RESULT_TEMPLATE = '''
<?xml version="1.0" encoding="utf-16"?>
<resultDetails xmlns:psr="http://www.pearson.com/services/SimpleResults/data/v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:psa="http://www.pearson.com/services/SimpleAssessment/data/v1p0" xmlns:tos="http://www.pearson.com/xsd/tpiOutcomesService_v1p0" xmlns:cor="http://www.imsglobal.org/services/lti/xsd/CoreOutcomesService_bv1p0">
    <psr:totalDuration></psr:totalDuration>
    <psr:parts>
        <psr:simpleSectionResult>
            <psr:parts>
              <psr:simpleItemResult>
                  <psr:itemBindingId>problem_guid</psr:itemBindingId>
                  <psr:itemId>${problemNumber}</psr:itemId>
                  <psr:itemScore>${score}</psr:itemScore>
                  <psr:duration>${duration}</psr:duration>
                  <psr:submissionCount>${submissionCount}</psr: submissionCount>
              </psr:simpleItemResult>
            </psr:parts>
        </psr:simpleSectionResult>
    </psr:parts>
</resultDetails>
'''

if __name__ == '__main__':
    params = TEST_TPI_PARAMS
    params.update(TEST_EXTRA_PARAMS)
    params['extensionBody'] = cgi.escape(Template(SIMPLE_ITEM_RESULT_TEMPLATE).substitute(params))
    params['messageBody'] = Template(REPLACE_RESULT_TEMPLATE).substitute(params)
    result = Template(WRAPPER_TEMPLATE).substitute(params)
    print result
