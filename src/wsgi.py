"""
WSGI config for sharing_things project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

# path a donde esta el manage.py de nuestro proyecto Django
sys.path.append('/home/admin/sharing_things/sharing_things/')

# referencia (en python) desde el path anterior al fichero settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

# prevenimos UnicodeEncodeError
os.environ.setdefault('LANG', 'en_US.UTF-8')
os.environ.setdefault('LC_ALL', 'en_US.UTF-8')

# activamos nuestro virtualenv
activate_this = '/home/admin/sharing_things/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

application = get_wsgi_application()
