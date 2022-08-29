from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("login", views.professorlogin, name='professorlogin'),
    path("", views.professor, name='professor'),



]