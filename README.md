[![Build Status](https://travis-ci.org/botswana-harvard/edc-calendar.svg)](https://travis-ci.org/botswana-harvard/edc-calendar)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-calendar/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/edc-calendar?branch=develop)

# edc-calendar


Integrates the django-scheduler app to manipulate appointments from edc-appointment

## How to install

pip install -r requirements.txt

# edit settings.py

Add 'schedule' and 'djangobower' to INSTALLED_APPS
Run: npm install -g bower
Add 'djangobower.finders.BowerFinder' to STATICFILES_FINDERS
Specify the path to the components root: BOWER_COMPONENTS_ROOT = '/PROJECT_ROOT/components/'
Add 'jquery' and 'bootstrap' to BOWER_INSTALLED_APPS 
Install bower depedencies: python manage.py bower install

