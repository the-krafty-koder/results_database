from django import forms
from .models import *

username = "Premier High"

def get_username(user):
    global username
    username = user

def get_class(username):
    return [(y,y) for y in (x.class_name for x in Institution.objects.find(username).classes)]
def get_streams(username):
    return [(y,y) for y in (x.stream_name for x in Institution.objects.find(username).classes[0].streams)]

class submit_form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(submit_form, self).__init__(*args, **kwargs)
        self.fields['classes'] = forms.ChoiceField(
            choices=get_class(username) )
        self.fields['streams'] = forms.ChoiceField(
            choices=get_streams(username) )


    exam_name = forms.CharField(max_length=50)
    exam_year = forms.CharField(max_length=50)
    exam_term = forms.CharField(max_length=50)
    exam_cat = forms.CharField(max_length=50)
    classes = forms.ChoiceField(choices=get_streams(username))
    streams = forms.ChoiceField(choices=get_class(username))

class upload_form(submit_form):
    file = forms.FileField()

class edit_student_form(forms.Form):
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    adm = forms.IntegerField(label="Admission Number")
    kcpe = forms.CharField(max_length=30,label="KCPE")
    contact = forms.IntegerField(label="Phone Number")
    email  = forms.EmailField(max_length=30,label="E-mail")

class new_student_form(forms.Form):
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    adm = forms.IntegerField(label="Admission Number")
    kcpe = forms.CharField(max_length=30,label="KCPE")
    contact = forms.IntegerField(label="Phone Number")
    email  = forms.EmailField(max_length=30,label="E-mail")

class create_subject_form(forms.Form):
    name = forms.CharField(max_length=30)
    type = forms.ChoiceField(choices = [("Compulsory","Compulsory"),("Sciences","Sciences"),("Humanities","Humanities"),("Technical 1","Technical 1"),("Technical 2","Technical 2")])
    group = forms.CharField(max_length=30)
    code = forms.CharField(max_length=30)

class create_class_form(forms.Form):
    name = forms.CharField(max_length=30)

class edit_class_form(forms.Form):
    name = forms.CharField(max_length=30,label="Class Name")

class add_stream_form(forms.Form):
    form_name = forms.CharField(max_length = 10)
    stream_name = forms.CharField(max_length=20)
    class_teacher = forms.CharField(max_length=20,label="Classteacher Name")

#class create_class_form(forms.Form):
