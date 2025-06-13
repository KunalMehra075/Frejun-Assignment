#!/bin/bash

# Create Django project
django-admin startproject roombooking .

# Create apps
python manage.py startapp users
python manage.py startapp bookings
python manage.py startapp rooms

# Create necessary directories
mkdir -p roombooking/templates
mkdir -p roombooking/static 