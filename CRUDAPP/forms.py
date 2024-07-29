from django.contrib.auth.models import User
from django import forms

class Login_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

# class ProfileEdit_form(forms.ModelForm):
#     class Meta:
#         model = UserBio
#         fields = ('')