# foodroller
Django app to manage your favorite recipes and to get suggestions what to eat the next days.


## Build
[![Build
Status](https://travis-ci.org/zenith0/foodroller.svg?branch=master)](https://travis-ci.org/zenith0/foodroller)

## Prerequisites
Python 3.4+ 
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

## TODOs:

### v1:

* Unittests for views

* Remove django admin and add functionality to edit food to the food template

* Add user management


### v2:

* provide API to add food from mobile client

* import recipes from chefkoch.de
