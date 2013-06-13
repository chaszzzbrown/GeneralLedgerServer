'''
Created on Jun 12, 2013

@author: charlieb
'''

import datetime
from string import Template

WRAPPER_TEMPLATE = '''

<tos:outcomeMessage xsi:schemaLocation="http://www.pearson.com/xsd/tpiOutcomesService_v1p0 tpiOutcomesService_v1p0.xsd"
xsi:type="tos:OutcomeMessage.Type" xmlns:cor="http://www.imsglobal.org/services/lti/xsd/CoreOutcomesService_bv1p0"
xmlns:tos="http://www.pearson.com/xsd/tpiOutcomesService_v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <tos:messageInfo>
      <tos:dataSource>$sourceGuid</tos:dataSource>
      <tos:dataSourceName>$sourceName</tos:dataSourceName>
      <tos:transactionId>$transactionId</tos:transactionId>
      <tos:timestamp>$timeStamp</tos:timestamp>
      <tos:partnerId>$partnerId</tos:partnerId>
      <tos:institutionId>$institutionId</tos:institutionId>
      <tos:contextIdentifier>$contextId</tos:contextIdentifier>
   </tos:messageInfo>
   $messageBody
 </tos:outcomeMessage>
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
    
    