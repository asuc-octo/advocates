# SAO Web Application

## About

This web application is designed to manage a bunch of SAO stuff. This includes things like user login and creation, caseworker management, caseworker assignment, case edits, file management, and email forwarding. 

## Working with the code

In order to work with the code, we want to start by creating a virtual environment with the following commands: 

'''
$ pip install virtualenv
$ cd advocates
$ virtualenv my_project
$ source my_project/bin/activate
'''

Great. Now that we have a virtual environment up and running, let us install all of the requirements that we need. 

'''
$ pip install -r requirements.txt
'''

Fantastic. Now let's get everything up and running
'''
$ python manage.py makemigrations
$ python manage.py migrate
'''

Good. Now, let's launch the server and explore around. 

'''
$ python manage.py runserver
'''