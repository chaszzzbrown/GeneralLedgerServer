import urllib2, base64

TARGET_URL = 'http://ifigs.redhillstudios.com'
def tryIt(userName=None, password=None):
    request = urllib2.Request(TARGET_URL)
    if (userName):
        base64string = base64.encodestring(userName+':'+password)
        request.add_header('Authorization', 'Basic '+base64string)
    try:
        result = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        result = err
    print 'Result code: %s'%result.code
        

    
