from django.http import JsonResponse
from django.shortcuts import _get_queryset
import uuid
from os.path import join


# my custom Functions.

def check_form_integrity(form_determinants: list, post_data: dict) -> bool:
    """
    it matches the form_determinants with the Form's POST & FILES Data to see
    if it have the right data or not. this function is simply looking for a given
    list of strings in a given Dictionary & if all the strings matched keys in the dictionary,
    it'll return True, else return False. this function is best used to choose which form is right
    for the POST data. \n
    :param form_determinants: list of strings.
    :param post_data: Dictionary (for example: request POST & FILES data).
    :return: bool = True or False.
    """
    ts = all([x in post_data for x in form_determinants])
    print('ts= ', ts, '\n determinants= ', form_determinants, '\n post_data= ', post_data)
    return ts
# an example of the above function:
# 1. forms.py file :
# class test_modelForm(forms.ModelForm):
#    # you have to write an input element that have name the same as field_1_name
#    form_determinants = ['field_1_name', 'field_n_name']
#
# 2. views.py file :
# class some_class_based_view(ListView):
#   def post(self, request, *args, **kwargs):
#        data = {**request.POST, **request.FILES}  # merging two dictionaries.
#        if check_form_integrity(test_modelForm.form_determinants, data):
#            self.form = test_modelForm()


# custom function that substitute get_list_or_404 cuz i don't want 404.
def filter_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        obj_list = list(queryset.filter(*args, **kwargs))
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_list_or_404() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    except DoesNotExist:
        return None
    if not obj_list:
        obj_list = None
    return obj_list


def get_file_path(file_dir: str):
    """
    This function is useful for join the file name to the desired directory name. \n
    :param file_dir: string contains the desired directory to save the file into.
    :return: Anonymous function that takes model instance and filename from django.
    """
    # extension = filename.split('.')[-1]
    # filename = "%s.%s" % (uuid.uuid4(), ext)
    # return join(file_dir, filename)
    global give_path

    def give_path(instance, filename):
        return join(file_dir, "%s.%s" % (uuid.uuid4().int, filename.split('.')[-1]))

    return give_path


# Custom Mixins

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(
                {'pk': self.object.pk,}
            )
        return response
