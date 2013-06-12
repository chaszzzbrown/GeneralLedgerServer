#!/home/ch/chasbrown.com/local/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home/re/redhillstudios.com/projects/glservice/glservice")

# Switch to the directory of your project. (Optional.)
os.chdir("/home/re/redhillstudios.com/projects/glservice/glservice")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "glservice.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
