from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from .models import Profile


class UserForm(forms.ModelForm):
    """Form for editing info in User model"""
    confirm_email = forms.EmailField(label="Confirm Email",
                                     required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['email'] != cleaned_data['confirm_email']:
            raise forms.ValidationError("E-mails do not match!")
        return cleaned_data


class PasswordForm(forms.ModelForm):
    """Form for editing password in User model"""
    confirm_password = forms.CharField(label='Confirm Password',
                                       max_length=256)

    class Meta:
        model = User
        fields = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data['password'] !=
                cleaned_data['confirm_password']):
            raise forms.ValidationError("Passwords do not match!")
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

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     try:
    #         # w, h = get_image_dimensions(avatar)
    #
    #         # validate dimensions
    #         # max_width = max_height = 100
    #         # if w > max_width or h > max_height:
    #         #     raise forms.ValidationError(
    #         #         u'Please use an image that is '
    #         #         '%s x %s pixels or smaller.' % (max_width, max_height))
    #
    #         # validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                                         'GIF or PNG image.')
    #
    #         # validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'Avatar file size may not exceed 20k.')
    #
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         pass

        return avatar

