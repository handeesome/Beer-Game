"""SE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views


'''*******************************
Add paths to each of the html pages.

********************************'''
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('goindex', views.goindex, name='goindex'),
    path('instructor_registration', views.instructor_registration, name='instructor_registration'),
    path('ins_reg', views.ins_reg, name = 'ins_reg'),
    path('ins_log', views.ins_log, name = 'ins_log'),
    path('stu_log', views.stu_log, name = 'stu_log'),
    path('cus_reg', views.cus_reg, name = 'cus_reg'),
    path('cus_log', views.cus_log, name = 'cus_log'),

]
