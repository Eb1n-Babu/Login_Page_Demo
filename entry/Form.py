import re

from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    @staticmethod
    def validate_strong_password(password):
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[^A-Za-z0-9]', password):  # special character
            raise forms.ValidationError("Password must contain at least one special character")

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        if password:
            self.validate_strong_password(password)
        return cleaned_data
