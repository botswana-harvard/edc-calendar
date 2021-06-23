# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(
    name='edc-calendar',
    version='0.1.4',
    author=u'Software Engineering & Data Management',
    author_email='se-dmc@bhp.org.bw',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/botswana-harvard/edc-calendar',
    license='GPL licence, see LICENCE',
    description='EDC calendar for events management.',
    long_description=README,
    zip_safe=False,
    keywords='django calendar',
    install_requires=[
        'django',
        'django[argon2]',
        'django-simple-history',
        'django-js-reverse',
        'django-logentry-admin',
        'django-debug-toolbar',
        'django-extensions',
        'python-dateutil',
        'docutils',
        'model_mommy',
        'Faker',
        'pytz',
        'arrow',
        'python-memcached',
        'pymysql',
        'tqdm',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
