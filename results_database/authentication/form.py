from django import forms

class login_form(forms.Form):

    name = forms.CharField(max_length=45)
    institution_name = forms.CharField(max_length=50)
    attrs = {
        "type": "password"
    }

    password = forms.CharField(min_length=8,widget=forms.TextInput(attrs=attrs))

class signup_form(forms.Form):
    user_name = forms.CharField(max_length=45)
    email = forms.EmailField()
    institution_name = forms.CharField(max_length=45)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(min_length=8,widget=forms.TextInput(attrs=attrs))

class institution_form(forms.Form):
    institution_name = forms.CharField(max_length=45)
    address = forms.CharField(max_length=45)
    website = forms.CharField(max_length=45)
    telephone = forms.CharField(max_length=45)
