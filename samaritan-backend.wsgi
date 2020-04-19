#samaritan-backend.wsgi
import sys
sys.path.insert(0, '/var/www/html/samaritan-backend')

from samaritan-backend import app as application