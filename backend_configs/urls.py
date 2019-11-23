"""backend_configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from secondBrainBackend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('add_person/',views.AddPerson.as_view()),
    path('add_information/',views.AddInformation.as_view()),
    path('identify_person/',views.IdentifyPerson.as_view()),
    path('results_person/',views.ResultsPerson.as_view()),
    path('search_tags/',views.SearchTags.as_view()),
    path('result_tags/',views.ResultTags.as_view()),
    path('show_persons/',views.ShowPersons.as_view()),
]
