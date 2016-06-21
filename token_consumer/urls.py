from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, 
        name='token_login', kwargs={
            'template_name': 'token_consumer/login.html'}),
    url(r'^logout/$', views.token_logout, name='token_logout'),
]
