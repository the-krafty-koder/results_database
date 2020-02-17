"""results_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from submission.views import *
from authentication.views import *
from wkhtmltopdf.views import PDFTemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('load_csv',load_csv,name="load_csv"),
    path('load_results',load_results,name="load_results"),
    path('load_base',load_base,name="load_base"),
    path('load_load',load_load,name="load_loader"),
    path('load_list',load_list,name="load_class_list"),
    path('load_student',load_student,name="load_student_results"),
    path('load_stream/<str:form_name>/<str:stream_name>',load_stream,name="load_stream"),
    path('load_student_db',load_student_db,name="load_students"),
    path('view_student_db/<str:form_name>/<str:stream_name>/',view_student_db,name="view_students"),
    path('add_student',new_student,name="add_student"),
    path('edit_student/<str:form_name>/<str:stream_name>/<str:student_name>',edit_student,name="edit_student"),
    path('edit_stream/<str:form_name>/<str:stream_name>/',edit_stream,name="edit_stream"),
    path('load_dashboard',load_dashboard,name="load_dashboard"),
    path('login',loginto,name="login"),
    path('signup',signup,name="signup"),
    path('create_institution',create_institution,name="create_institution"),

]
