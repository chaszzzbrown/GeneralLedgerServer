'''
Created on Jun 12, 2013

@author: charlieb
'''

import datetime
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


WRAPPER_TEMPLATE = '''

<tos:outcomeMessage xsi:schemaLocation="http://www.pearson.com/xsd/tpiOutcomesService_v1p0 tpiOutcomesService_v1p0.xsd"
xsi:type="tos:OutcomeMessage.Type" xmlns:cor="http://www.imsglobal.org/services/lti/xsd/CoreOutcomesService_bv1p0"
xmlns:tos="http://www.pearson.com/xsd/tpiOutcomesService_v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <tos:messageInfo>
      <tos:dataSource>${custom_tool_proxy_guid}</tos:dataSource>
      <tos:dataSourceName>${custom_originating_partner}</tos:dataSourceName>
      <tos:transactionId>${transactionId}</tos:transactionId>
      <tos:timestamp>$timeStamp</tos:timestamp>
      <tos:partnerId>${custom_partner_id}</tos:partnerId>
      <tos:institutionId>${custom_institutionId}</tos:institutionId>
      <tos:contextIdentifier>$contextId</tos:contextIdentifier>
   </tos:messageInfo>
   $messageBody
 </tos:outcomeMessage>
 '''

REPLACE_RESULT_TEMPLATE = '''
   <cor:replaceResultRequest>
      <cor:sourcedId>b53f0a9c-1c0d-489e-a361-d148eb5ea33e</cor:sourcedId>
      <cor:resultRecord>
         <cor:sourcedId>b53f0a9c-1c0d-489e-a361-d148eb5ea33e</cor:sourcedId>
         <cor:result>
            <cor:statusofResult>
               <cor:displayName>Quiz</cor:displayName>
            </cor:statusofResult>
            <cor:personSourcedId>a1df4b66-7930-4330-be14-03d52d74dda1_sakai_unicon</cor:personSourcedId>
            <cor:lineItemSourcedId>d4ea086e-b904-4dc5-b1b0-955a1c245497</cor:lineItemSourcedId>
            <cor:date>2010-08-31T12:34:18</cor:date>
            <cor:resultScore>
               <cor:language>en-US</cor:language>
               <cor:textString>7</cor:textString>
            </cor:resultScore>
            <cor:dataSource>f3ab6f04-f7d3-4375-b274-60f4576d960f</cor:dataSource>
         </cor:result>
      </cor:resultRecord>
   </cor:replaceResultRequest>
'''

DATA_SOURCE_GUID = 'f3ab6f04-f7d3-4375-b274-60f4576d960f'
DATA_SOURCE_NAME = 'accountingXL'
PARTNER_ID = 'redhill'
INSTITUTION_ID = 'accounting'

class OutcomeWrapper:
    
    def __init__(self, transactionId, contextIdentifier):
        self.timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        self.transactionId = transactionId
        self.contextIdentifier = contextIdentifier
        self.content = []
        pass
    
    def asStrippedXML(self):
        return self.asXML().replace('\n','').replace('\t', '')
    
    def asXML(self):
        contentXML = ''
        if (self.content):
            for block in self.content:
                contentXML += block.asXML+'\n\n'
        result = Template(WRAPPER_TEMPLATE)
        result = result.substitute(sourceGuid=DATA_SOURCE_GUID,
                                   sourceName=DATA_SOURCE_NAME,
                                   transactionId=self.transactionId,
                                   timeStamp=self.timestamp,
                                   partnerId=PARTNER_ID,
                                   institutionId=INSTITUTION_ID,
                                   contextId=self.contextIdentifier,
                                   messageBody=contentXML
                                   )
        return result

if __name__ == '__main__':
    wrapper = OutcomeWrapper(15, 'abcd-87654-123748')
    f = open('textout.xml', 'w')
    f.write(wrapper.asStrippedXML())
    f.close()
    
    