"""courseProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name = 'home'),
    path('administrator/', admin.site.urls),
    path('professors/search/', views.professors_search),
    path('professors/salaries', views.professors_salaries),
    path('professors/students', views.professors_studenst),
    path('student',  include('student.urls')),
    path('professor', include('professor.urls')),
    path('administrator',include('administrator.urls')),
    path('registeruser', views.registeruser, name = 'registeruser')
]
