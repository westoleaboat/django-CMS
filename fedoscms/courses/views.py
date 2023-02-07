# from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# restricting access to class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class OwnerMixin(object):
    '''
    Override the get_queryset() method of the view to retrieve only courses created by the current user.

    OwnerMixin class can be used for views that interact with any model that contains an owner attribute.
    '''

    def get_queryset(self):
        # get base QuerySet
        qs = super().get_queryset()
        # filter objects by the owner attribute to retireve objects
        # that belong to the current user (request.user)
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    '''
    Implements the form_valid() method, used by views that use ModelFromMixin, that is views with forms or model forms such as CreateView and UpdateView.form_valid() is executed when the submitted form is valid. The default method is 
    saving the instance (for model forms) and redirecting the user to success_url.
    Override this method to automatically set the current user in the owner attribute of the object being saved. By doing so, you set the owner for an object automatically when it is saved 
    '''

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    '''
    inherits from OwnerMixin and provides the following attributes for child views:
        -model: model used for QuerySets; used by all views.
        -fields: fields of the model to build the model form of the CreateView and Updateview views.
        -success_url: Used by CreateView, UpdateView, and DeleteView to redirect the user after the form is successfully submitted or the object is deleted.
    '''
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    '''
    Mixin with the template_name attribute
        -template_name: the template you will use for the CreateView and UpdateView views.
    '''
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    '''
    Lists the courses created by user, defines a specific template_name attribute for a template to list courses
    '''
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    '''
    Uses a model form to create a new Course object. It uses the fields defined in OwnerCourseMixin to build a model form and also subclasses CreateView. it uses the template defined in OwnerCourseEditMixin
    '''
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    '''
    Allows the editing of an existing Course object. It uses the fields defined in OwnerCourseMixin to build a model form and also subclases UpdateView. It uses the template defined in OwnerCourseEditMixin.
    '''
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    '''
    It defines a specific template_name attribute for a template to confirm the course deletion.
    '''
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


# class ManageCourseList(ListView):
#     '''
#     This view inherits from Django's generic ListView.
#     Override the get_queryset() method of the view to retrieve only courses created by the current user.
#     '''
#     model = Course
#     template_name = 'course/manage/course/list.html'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(owner=self.request.user)
