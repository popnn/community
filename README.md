# popN community

A thread based community platform which supports multiple discussion threads which can be controlled by specific users and provide full control of the discussion to the manager of the thread.

# Requirements
1. Python3
2. python-pillow - pip install pillow
3. Django
4. Django-pwa-Webpush - pip install django-pwa-webpush
5. Django bootstrap - pip install django-bootstrap-static

# How To Install

1. Clone this repository on the system
2. Cd into the repository
3. Run - python3 manage.py migrate
4. Add your domain to /popN/settings.py - Allowed Hosts - add your domain
5. Run the server - python3 manage.py runserver IP_ADDRESS:PORT
