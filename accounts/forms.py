from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    """Form for editing info in User model"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class EmailForm(forms.ModelForm):
    """Form for editing email in User model"""
    confirm_email = forms.EmailField(label="Confirm Email",
                                     required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['email'] != cleaned_data['confirm_email']:
            raise forms.ValidationError("E-mails do not match!")
        return cleaned_data


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

