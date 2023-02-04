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

register the models in the admin site
edit admin.py with @admin decorators

create superuser

pipenv install gunicorn

self-signed public-key certificates

openssl req -x509 -nodes -days 3650 -newkey ec:<(openssl exparam -name prime256v1) -keyout private_key.pem -out certificate.pem

in my case, this cert in default localhost port 8000 didnt work (i think) because i had another cert for a django app in port 8000, making error in ssl request etc. 
when filling information for creating self-signed certificate, specify the localhost:port option, in my case 8080

Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:CO
Locality Name (eg, city) []:Colorado
Organization Name (eg, company) [Internet Widgits Pty Ltd]:FedosCMS INC.
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost:8080
Email Address []:admin@fedoscms.com

in django settings.py add '0.0.0.0' to ALLOWED HOSTS setting.

if necesary, move certfile and private kry files to your project folder and run gunicorn 

gunicorn fedoscms.wsgi -b :8080 --keyfile private_key.pem --certfile certificate.pem

check the localhost:8080/admin to see if static files are shown
if not, run

python manage.py collectstatic

install whitenoise

pipenv install whitenoise

add the following to settings.py
https://stackoverflow.com/questions/12800862/how-to-make-django-serve-static-files-with-gunicorn

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

now you should be able to access your development server through https (which is great) and serve static files

# using fixtures to provide initial data for models

Sometimes, you might want to prepopulate your database with hardcoded data. 
This is useful for automatically including initial data in the project setup, instead of 
having to add it manually. Django comes with a simple way to load and dump data 
from the database into files that are called fixtures. Django supports fixtures in JSON, 
XML, or YAML formats. You are going to create a fixture to include several initial 
Subject objects for your project.

open localhost:8080/admin/courses/subject and add several subjects,
after that run 

python manage.py dumpdata courses --indent=2

The dumpdata command dumps data from the database into the standard 
output, serialized in JSON format by default. The resulting data structure 
includes information about the model and its fields for Django to be able 
to load it into the database.

You can limit the output to the models of an application by providing the application 
names to the command, or specifying single models for outputting data using the 
app.Model format. You can also specify the format using the --format flag. By 
default, dumpdata outputs the serialized data to the standard output. However, you 
can indicate an output file using the --output flag. The --indent flag allows you 
to specify indentation. For more information on dumpdata parameters, run python 
manage.py dumpdata --help.

You can remove the subjects from administration site,
then, you can load the fixture into the database using 

python manage.py loaddata subjects.json

all subject objects included in the fixture are loaded into the database

By default, Django looks for files in the fixtures/ directory of each application, but 
you can specify the complete path to the fixture file for the loaddata command. You 
can also use the FIXTURE_DIRS setting to tell Django additional directories to look in 
for fixtures.

# creating models for diverse content