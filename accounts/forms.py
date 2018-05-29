from datetime import datetime
from django import forms
from django.contrib.auth.models import User

from .models import Profile

import logging
logger = logging.getLogger(__name__)

import dns.resolver, dns.exception


class UserForm(forms.ModelForm):
    """Form for editing info in User model"""
    confirm_email = forms.EmailField(label="Confirm Email",
                                     required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_confirm_email(self):
        email = self.cleaned_data['email']
        confirm_email = self.cleaned_data['confirm_email']

        # Check to make sure email inputs match.
        if email != confirm_email:
            raise forms.ValidationError("E-mails do not match!")

        # Check to make sure email has a valid domain, by checking for
        # MX records on the email domain (requires dnspython).
        domain = confirm_email.split('@')[1]
        try:
            logger.debug('Checking domain %s', domain)
            results = dns.resolver.query(domain, 'MX')

        except dns.exception.DNSException:
            logger.debug('Domain does not exist.')

            raise forms.ValidationError("That domain could"
                                        " not be found.")

        return confirm_email


class ProfileForm(forms.ModelForm):
    """Form for editing info in Profile model"""
    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(
            datetime.now().year - 100, datetime.now().year + 1
        ))
    )
    bio = forms.CharField(required=False, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('birthday', 'bio', 'avatar')

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) < 10 and len(bio) != 0:
            raise forms.ValidationError(
                "Bio must be at least 10 characters!"
            )
        return bio

