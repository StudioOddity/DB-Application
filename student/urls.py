from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("login", views.studentlogin, name='studentlogin'),
    path("", views.students, name='students'),



]