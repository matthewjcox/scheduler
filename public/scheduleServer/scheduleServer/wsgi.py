"""
WSGI config for scheduleServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os
print(os.getcwd())
exec(open("../../env/bin/activate_this.py").read(),dict(__file__="../../env/bin/activate_this.py"))
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduleServer.settings')

application = get_wsgi_application()
