from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

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
    # specify that the ordering is calculated with respect to the course
    # This means that the order for a new module will be assigned by adding 1 to the last module of the same Course object.
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        # return self.title
        return f'{self.order}. {self.title}'

# Content model that represents the modules' contents.


class Content(models.Model):
    '''
    This is the Content model. A module contains multiple contents, so you define a 
    ForeignKey field that points to the Module model. You also set up a generic relation to associate objects from different models that represent different types of content. Remember you need three different fields to set up a generic relation, in the Content model, these are content_type, object_id and item.

    Only the content_type and object_id fields have a corresponding column in the 
    database table of this model. The item field allows you to retrieve or set the related object directly, and its functionality is built on top of the other two fields.
    You are going to use a different model for each type of content. Your content models will have some common fields, but they will differ in the actual data they can store.
    '''
    # A ForeignKey that points to the Module model.
    module = models.ForeignKey(
        Module, related_name='contents', on_delete=models.CASCADE)
    # Set up a generic relation to associate objects from different models

    # A ForeignKey field to the ContentType model.
    # limit_choices_to argument to limit the ContentType objects that can be used for
    # the generic relation. use model__in field lookup to filter the query to the
    # ContentType objects with a model attribute that is 'text','video','image', or 'file'
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in': ('text', 'video', 'image', 'file')})
    # A PositiveIntegerField to store the primary key of the related object
    object_id = models.PositiveIntegerField()
    # A GenericForeignKey field to the related object combining the two previous fields.
    item = GenericForeignKey('content_type', 'object_id')
    # order is calculated with respect to the module field.
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):  # Abstract mode, set in Meta class
    '''
    In this model you define the owner, title, created, and updated fields. These commonn fields will be used for all types of content.
    '''
    # Owner store which user created the content. Since is defined in abstract class, you need a different related_name for each sub-model. Using '%(class)s' the related_name for each child model will be generated automatically, e.g. (text_related, file_related, image_related, video_related)
    owner = models.ForeignKey(
        User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # no database table associated with abstract model.

    def __str__(self):
        return self.title

# Four different content models that inherit from the ItemBase abstract model.
# Each child model contains the fields defined in the ItemBase class
# in addition to its own fields. A database tabl will be created for the Text,
# File, Image, and Video models respectively


class Text(ItemBase):
    ''' Store text content. '''
    content = models.TextField()


class File(ItemBase):
    ''' Store files, such as PDFs '''
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    ''' Store image files '''
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    ''' Store videos, you use an URLField to provide a video URL in order to embed it '''
    url = models.URLField()
