from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveBigIntegerField):
    '''
    This is your custom OrderField. It inherits from the PositiveIntegerField
    field provided by Django. Your OrderField field takes an optional for_fields
    parameter that allows you to indicate the fields that the order has to be calculated with respect to.
    Your field overrides the pre_save() method of the PositiveIntegerField field, 
    which is executed before saving the field into the database. 
    In this method, you perform the following actions

    When you create custom model fields, make them generic. Avoid 
    hardcoding data that depends on a specific model or field. Your 
    field should work on any model.
    '''

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # chech whether a value already exists for this field in the model instance.
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # build a QuerySet to retrieve all objects for the field's model.
                # You retrieve the model class the field belongs to by accessing self.model
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field)
                             for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                # if object is found, add 1 to the highest order found
                value = last_item.order + 1
                # if no object is found,
            except ObjectDoesNotExist:
                #  assume object is first one, assign the order of 0 to it.
                value = 0
            # assign the calculated order to the field's value in the model instance using setattr and return it
            setattr(model_instance, self.attname, value)
            return value
        # if the model instance has a value for the current field, you use it instead of calculating
        else:
            return super().pre_save(model_instance, add)
