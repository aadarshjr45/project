from django.contrib import admin
from django.urls import path

from employer.views import(
    post_job,
    application,
    dashboard,
    jobs,
    job_detail,
    job_edit,
    job_delete,
    accept_application,
    reject_application,
    add_company,
    view_company,
    edit_company, 
    delete_company,
    profile_view,
    profile_edit
   
)

app_name = "employer"

urlpatterns = [
    path('post_job/company <int:id>', post_job, name='post_job'),
    path('applications/', application, name='applications'),
    path('dashboard/', dashboard, name='dashboard'),
    path('jobs/', jobs, name='jobs'),
    path('jobs/details/job_id <int:job_id>', job_detail, name='job_detail'),
    path('jobs/job_id <int:id>/edit/', job_edit, name='job_edit'),
    path('jobs/delete/', job_delete, name='job_delete'),
    path('accept/application_id <int:id>/', accept_application, name='accept_application'),
    path('reject/application_id <int:id>/', reject_application, name='reject_application'),
    path('add_company/', add_company, name='add_company'),
    path('view_company/', view_company, name='view_company'),
    path('delete_company/', delete_company, name='delete_company'),
    path('edit_company/id <int:id>/', edit_company, name='edit_company'),
    path("profile/user_id  <int:id>/",profile_view, name='profile'),
    path("profile/edit/user_id  <int:id>/",profile_edit, name='profileedit'),


]
