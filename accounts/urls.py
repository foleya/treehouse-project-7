from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', login_required(views.sign_out), name='sign_out'),
    url(r'profile/$', login_required(views.profile), name='profile'),
    url(r'profile/edit/$',
        login_required(views.profile_edit),
        name='profile_edit'),
    url(r'profile/change_email/$',
        login_required(views.change_email),
        name='change_email'),
    url(r'profile/change_password/$',
        login_required(views.change_password),
        name='change_password'),
]

