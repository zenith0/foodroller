# foodroller
Django app to manage your favorite recipes and to get suggestions what to eat the next days.

## Prerequisites
Python 3.x 
Developed and tested with Python 3.5 and Django 1.9

## Installation
* Get the source
* activate virtualenv: 
$ virtualenv -p python3 foodroller 
$ cd foodroller 
$ . bin/activate
* install dependencies:
$ pip install -r requirements.txt
* Sync DB:
$ python manage.py migrate
* Create Superuser:
$ python manage.py createsuperuser
* Start:
$ python manage.py runserver

You can reach foodroller in your browser localhost:8000 and the admin interface @ localhost:8000/admin
