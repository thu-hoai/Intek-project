from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Report


class UserConnectionForm(UserCreationForm):
    """A User Connection Form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "User name",
                "class": "main_box_form_email_input",
                "autocomplete": "off",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Password",
                "class": "main_box_form_password_input",
                "autocomplete": "off"
            }
        )


class ReportForm(forms.ModelForm):
    """A Report Creation Form"""
    class Meta:
        model = Report
        fields = ['name', 'latitude', 'longitude', 'altitude', 'accuracy']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "placeholder": "Report Name",
                "class": "report_form_input",
            }
        )
        self.fields["latitude"].widget.attrs.update(
            {
                "placeholder": "Latitude",
                "class": "report_form_input",
            }
        )
        self.fields["longitude"].widget.attrs.update(
            {
                "placeholder": "Longitude",
                "class": "report_form_input",
            }
        )
        self.fields["altitude"].widget.attrs.update(
            {
                "placeholder": "Altitude",
                "class": "report_form_input",
            }
        )
        self.fields["accuracy"].widget.attrs.update(
            {
                "placeholder": "Accuracy",
                "class": "report_form_input",
            }
        )
