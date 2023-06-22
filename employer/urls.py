from django.contrib import admin
from django.urls import path

from employer.views import(
    post_job,
    application,
    dashboard,
    jobs,
    accept_application,
    reject_application,
    add_company,
    view_company,
    edit_company
   
)

app_name = "employer"

urlpatterns = [
    path('post_job/<int:id>', post_job, name='post_job'),
    path('applications/', application, name='applications'),
    path('dashboard/', dashboard, name='dashboard'),
    path('jobs/', jobs, name='jobs'),
    path('accept/<int:id>/', accept_application, name='accept_application'),
    path('reject/<int:id>/', reject_application, name='reject_application'),
    path('add_company/', add_company, name='add_company'),
    path('view_company/', view_company, name='view_company'),
    path('edit_company/id=<int:id>/', edit_company, name='edit_company'),

]
