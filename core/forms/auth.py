from django import forms

from core.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'is_active']
