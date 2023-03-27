from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car, Driver


def check_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        return "Must consist of 8 characters"
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        return "First 3 characters must be uppercase letters"
    if not license_number[3:].isdigit():
        return "Last 5 characters must be digits"
    return "OK"


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        resp = check_license_number(license_number)
        if resp != "OK":
            raise ValidationError(resp)

        return license_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        resp = check_license_number(license_number)
        if resp != "OK":
            raise ValidationError(resp)

        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"