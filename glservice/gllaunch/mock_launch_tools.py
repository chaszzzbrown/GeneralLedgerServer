'''
Created on Jun 18, 2013

@author: charlieb
'''

LAUNCH_TEMPLATE = '''

<html>
 <head>
 </head>
  <body>
  <h1>{title}</h1>
   <div id="ltiLaunchFormSubmitArea">
     <form action="http://localhost:8000/gllaunch/toolLaunch/"
      name="ltiLaunchForm" id="ltiLaunchForm" method="post" encType="application/x-www-form-urlencoded">
       {inputs}
    <input type="submit" value="Simulate Launch"/>
     </form>
    </div>
     <script language="javascript">
      // document.getElementById("ltiLaunchFormSubmitArea").style.display = "none";
      // document.ltiLaunchForm.submit();
     </script>
  </body>
</html>
'''

def construct_mock_html(launch_dict, title):
    inputs = ''
    for k,v in launch_dict.items():
        inputs += '          <input name="{key}" value="{val}" type="hidden" />\n'.format(key=k, val=v)
    return LAUNCH_TEMPLATE.format(inputs=inputs, title=title)
    
if __name__=='__main__':
    print construct_mock_html({'foo':-234561, 'bar':'aa23516-236749-23678'}, "Simulate TPI Launch, Test")