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
models.py in courses app
You plan to add different types of content to the course modules, such as text, 
images, files, and videos. Therefore, you need a versatile data model that allows 
you to store diverse content.
You are going to create a Content model that represents the modules' contents, and define a generic relation to associate any kind of content.

# using model inheritance
Django supports model inheritance. It works in a similar way to standard class 
inheritance in Python. Django offers the following three options to use model 
inheritance: #page 366
• Abstract models: Useful when you want to put some common information 
into several models.
• Multi-table model inheritance: Applicable when each model in the 
hierarchy is considered a complete model by itself.
• Proxy models: Useful when you need to change the behavior of a model, 
for example, by including additional methods, changing the default manager, 
or using different meta options.

# creating the content models
The Content model of your courses application contains a generic relation to 
associate different types of content with it. You will create a different model for each 
type of content. All content models will have some fields in common and additional 
fields to store custom data. You are going to create an abstract model that provides 
the common fields for all content models.

make migrations to include new models 

python manage.py makemigrations

Migrations for 'courses':
  courses/migrations/0002_content_file_image_text_video.py
    - Create model Video
    - Create model Text
    - Create model Image
    - Create model File
    - Create model Content

apply migrations
python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying courses.0002_content_file_image_text_video... OK

# creating custom model fields.
You need a field that allows you to define an order for objects. An easy way 
to specify an order for objects using existing Django fields is by adding a 
PositiveIntegerField to your models. Using integers, you can easily specify 
the order of objects. You can create a custom order field that inherits from 
PositiveIntegerField and provides additional behavior.
create fields.py in courses app

create a model migration that reflects the new order fields.

python manage.py makemigrations courses

You are trying to add a non-nullable field 'order' to content without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 0
You are trying to add a non-nullable field 'order' to module without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 0
Migrations for 'courses':
  courses/migrations/0003_auto_20230206_1224.py
    - Change Meta options on content
    - Change Meta options on module
    - Add field order to content
    - Add field order to module

apply new migrations 
python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying courses.0003_auto_20230206_1224... OK

test the new field. open the shell

python manage.py shell

create a new course

In [1]: from django.contrib.auth.models import User

In [2]: from courses.models import Module, Subject, Course

In [3]: user = User.objects.last()

In [4]: subject = Subject.objects.last()

In [5]: c1 = Course.objects.create(subject=subject, owner=user, title='Course 1', slug='course1')

You have created a course in the database. Now, you will add modules to the course 
and see how their order is automatically calculated. You create an initial module and 
check its order:

In [6]: m1 = Module.objects.create(course=c1, title='Module 1')

In [7]: m1.order
Out[7]: 0

OrderField sets its value to 0, since this is the first Module object created for the 
given course. You, create a second module for the same course:

In [8]: m2 = Module.objects.create(course=c1, title='Module 2')

In [9]: m2.order
Out[9]: 1

OrderField calculates the next order value, adding 1 to the highest order for existing 
objects. Let's create a third module, forcing a specific order:
In [10]: m3 = Module.objects.create(course=c1, title='Module 3', order=5)

In [11]: m3.order
Out[11]: 5

If you specify a custom order, the OrderField field does not interfere and the value 
given to order is used.
add a fourth module:
In [12]: m4 = Module.objects.create(course=c1, title='Module 4')

In [13]: m4.order
Out[13]: 6

The order for this module has been automatically set. Your OrderField field does 
not guarantee that all order values are consecutive. However, it respects existing 
order values and always assigns the next order based on the highest existing order.
Let's create a second course and add a module to it:

In [14]: c2 = Course.objects.create(subject=subject, title='Course 2', slug='course2', owner=user)

In [15]: m5 = Module.objects.create(course=c2, title='Module 1')

In [16]: m5.order
Out[16]: 0

To calculate the new module's order, the field only takes into consideration 
existing modules that belong to the same course. Since this is the first module 
of the second course, the resulting order is 0. This is because you specified for_
fields=['course'] in the order field of the Module model.

# Creating a CMS
Now that you have created a versatile data model, you are going to build the CMS. 
The CMS will allow instructors to create courses and manage their contents. You 
need to provide the following functionality:
• Log in to the CMS
• List the courses created by the instructor
• Create, edit, and delete courses
• Add modules to a course and reorder them
• Add different types of content to each module and reorder them

# Adding an authentication system
You are going to use Django's authentication framework in your platform. Both 
instructors and students will be instances of Django's User model, so they will be 
able to log in to the site using the authentication views of django.contrib.auth.

edited urls.py of fedoscms, now can access
localhost:8000/accounts/login/

# ~~Creating class-based views~~
# Using mixins for class-based views
build views to create, edit, delete courses
Mixins are a special kind of multiple inheritance for a class. You can use them 
to provide common discrete functionality that, when added to other mixins, allows 
you to define the behavior of a class. There are two main situations to use mixins:
-provide multiple optional features for a class
-use a particular feature in several classes

# working with groups and permissions
created Instructors group
created user fedor
added fedor to instructors group

# restrict access to class-based views
use LoginRequiredMixin and PermissionRequiredMixin
edit views.py

PermissionRequiredMixin checks that the user accessing the view has the 
permission specified in the permission_required attribute. Your views are 
now only accessible to users with proper permissions.

create URLs for these views. create urls.py inside courses application
include the created URLs patterns into main urls.py file of fedoscms project.

create templates for these views.

opening localhost:8000/accounts/login/?next=/course/mine loggin in with user from instructor group will redirect to /course/mine

Now you can create new courses, edit and delete them