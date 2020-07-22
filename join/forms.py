from django import forms
from .models import User,Userinformation
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class Registration(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    password=forms.PasswordInput()


class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields=(
            'name',
            'email',
            'password',
            'psw'
        )

class EditUserInformationForm(UserChangeForm):

    class Meta:
        model = Userinformation
        fields=(
            'image',
            'calculation_history',
            'posted_date'
        )



