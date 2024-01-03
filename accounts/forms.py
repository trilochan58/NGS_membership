from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from config.validators import validate_phone

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form in admin panel for creating user model."""

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """Form in admin panel for editing user model."""

    class Meta:
        model = CustomUser
        fields = ("email",)


class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    password = forms.CharField()
    confirm_password = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not validate_phone(phone):
            raise forms.ValidationError("Invalid Phone Number")
        return phone


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]
