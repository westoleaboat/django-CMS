from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# These are the initial Subject, Course and Module models.


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    '''
    Each course is divided into several modules. 
    Therefore, the Module model contains a ForeignKey 
    field that points to the Course model
    '''
    # who created this course
    owner = models.ForeignKey(
        User, related_name='courses_created', on_delete=models.CASCADE)
    # subject this course belongs to. Foreingkey points to subject model
    subject = models.ForeignKey(
        Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # slug of course, used in URLs later
    slug = models.SlugField(max_length=200, unique=True)
    # store and overview of the course
    overview = models.TextField()
    # automatic timestamp when course was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
