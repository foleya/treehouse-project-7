from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm,
                                       PasswordChangeForm)
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EmailForm, ProfileForm, UserForm


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request,
                     "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    """Displays user's profile"""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
@transaction.atomic
def profile_edit(request):
    """Edit information in User and Profile models"""
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated!')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.error(request, 'Please correct the error below')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def change_email(request):
    """Change email in User model"""
    if request.method == 'POST':
        email_form = EmailForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, 'Your e-mail was updated!')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.error(request, 'Please correct the error below')
    else:
        email_form = EmailForm(instance=request.user)
    return render(request, 'accounts/change_email.html', {
        'email_form': email_form,
    })


@login_required
@transaction.atomic
def change_password(request):
    """Change password in User model"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'You changed your password!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request, 'accounts/change_password.html', {'form': form}
    )

