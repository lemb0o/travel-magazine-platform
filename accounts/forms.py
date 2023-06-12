from django import forms
from .models import User
# from datetime import date
from django.contrib.auth import authenticate, login, logout
import re


# User Registration Form
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'password', 'password2',
                  ]
        # labels = {}
        widgets = {
            'password': forms.PasswordInput(
                attrs={'placeholder': 'Enter your password*'}
            ),
            'email': forms.EmailInput(
                attrs={'class': '', 'placeholder': 'Email*'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': '', 'placeholder': 'First Name*'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': '', 'placeholder': 'Last Name*'}
            ),
            'username': forms.TextInput(
                attrs={'class': '', 'placeholder': 'Username*'}
            ),
        }

    def clean(self, *args, **kwargs):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        username = self.cleaned_data['username']
        message = "Password must contain at least 2 digits,be at least 2 uppercase and be more than 6 letters."
        if len(password) < 6:
            raise forms.ValidationError(message)
        if sum(c.isdigit() for c in password) < 2:
            raise forms.ValidationError(message)
        if sum(c.isupper() for c in password) < 1:
            raise forms.ValidationError(message)
        if password != password2:
            raise forms.ValidationError('Password Must match.')
        if not re.search(r'^[\w.]+$', username):
            raise forms.ValidationError('Usernames can only use letters, numbers, underscores and periods.')
        return super(RegisterForm, self).clean()


# User Login Form
class LoginForm(forms.Form):  # forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("The user does not exist")
        else:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(LoginForm, self).clean()
