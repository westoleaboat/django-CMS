# django-CMS
Content management system with django

In this repo:

-create fixtures for your models
-Use model inheritance
-create custom model fields
-use class-based views and mixins
-build formsets
-manage groups and permissions
-Create a cms

setting up
create a virtual environment
pipenv shell
install django, pillow

steps to create a cms with django
create a new project with the following command
django-admin startproject fedoscms
enter new directory fedoscms and create a new application
cd fedoscms
django-admin startapp courses

edit settings.py of the fedoscms project and add courses to the installed apps setting
now the courses application is active for the project

lets define models for courses and course content
building course models

Your e-learning platform will offer courses on various subjects. Each course will 
be divided into a configurable number of modules, and each module will contain 
a configurable number of contents. The contents will be of various types: text, file, 
image, or video. The following example shows what the data structure of your 
course catalog will look like:
Subject 1
    Course 1
        Module 1
            Content 1 (image)
            Content 2 (text)
        module 2 
            content 3 (text)
            content 4 (file)
            content 5 (video)

build course modules: edit the models.py of the courses application
add initial subject, course, and module models.

create initial migration for this application
python manage.py makemigrations

Migrations for 'courses':
  courses/migrations/0001_initial.py
    - Create model Course
    - Create model Subject
    - Create model Module
    - Add field subject to course

apply migrations to the database
python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying courses.0001_initial... OK
  Applying sessions.0001_initial... OK

if the output is ... OK, the models of your courses application have been synced with the database.

