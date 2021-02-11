from .common import *

DEBUG = False
ALLOWED_HOSTS = ['https://mypa-django.herokuapp.com/']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_HSTS_SECONDS=3600
SECURE_HSTS_INCLUDE_SUBDOMAINS=False

# Configure logentries only if LOGENTRIES_KEY is defined in settings
if os.environ.get("LOGENTRIES_KEY", ''):
    LOGGING['handlers']['logentries'] = {
                'level': 'INFO',
                'token': os.environ.get("LOGENTRIES_KEY", ''),
                'class': 'logentries.LogentriesHandler',
                'formatter': 'verbose'
            }

    LOGGING['loggers']['mypa']['handlers'] = ['console', 'file', 'logentries']


########## CELERY
# In production, all tasks will be executed in the worker
CELERY_ALWAYS_EAGER = False
########## END CELERY

