from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("login", views.adminlogin, name='adminlogin'),
    path("", views.administrator, name='administrator'),



]