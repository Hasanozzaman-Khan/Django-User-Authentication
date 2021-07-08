from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomRegisterModel, ProfileModel


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomRegisterModel
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    class Meta:
        model=CustomRegisterModel
        fields=['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=ProfileModel
        fields=['image']
