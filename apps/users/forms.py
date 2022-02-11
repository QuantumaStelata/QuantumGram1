from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from . import models

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'class': 'text-center', 'placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.TextInput({'type': 'password', 'class': 'text-center', 'placeholder': 'Password'}), label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username')
            ),
            Row(
                Column('password'),
            ),
            Row(
                Column(
                    Submit('sign_in', 'Sign In', css_class='btn-respect btn-block')
                ),
                Column(
                    HTML("<a href='{% url 'users:registration' %}' class='btn btn-outline-respect btn-block'>Sign Up</a>")
                ),
                css_class='mt-2'
            )
        )
        

class RegistrationForm(forms.ModelForm):
    repeat_password = forms.CharField(widget=forms.TextInput({'type': 'password', 'class': 'text-center', 'placeholder': 'Repeat Password'}), label='')

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'username': '',
            'password': ''
        }
        help_texts = {
            'username': ''
        }
        widgets = {
            'first_name': forms.TextInput({'class': 'text-center', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput({'class': 'text-center', 'placeholder': 'Last Name'}),
            'email': forms.TextInput({'class': 'text-center', 'placeholder': 'Email'}),
            'username': forms.TextInput({'class': 'text-center', 'placeholder': 'Username'}),
            'password': forms.TextInput({'type': 'password', 'class': 'text-center', 'placeholder': 'Password'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['password'].min_lenght = 6
        self.fields['repeat_password'].min_lenght = 6

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name')
            ),
            Row(
                Column('email'),
            ),
            Row(
                Column('username'),
            ),
            Row(
                Column('password'),
                Column('repeat_password'),
            ),
            Row(
                Column(
                    Submit('sign_up', 'Sign Up', css_class='btn-respect btn-block')
                ),
                Column(
                    HTML("<a href='{% url 'users:login' %}' class='btn btn-outline-respect btn-block'>Sign In</a>")
                ),
                css_class='mt-2'
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            raise forms.ValidationError({'repeat_password': "Password mismatch"})

        return cleaned_data