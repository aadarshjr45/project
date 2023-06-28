from django.urls import path,include
from jobs.views import(
        job_list, 
        job_detail, 
        apply_job,
        job_delete,
        homepage, 
        search_view,
        job_edit,
        filter_view,
        main

       
)

app_name = "jobs"


urlpatterns = [
    path('', homepage, name='index'),
    path('jobs-list', job_list, name='job_list'),
    path('<int:job_id>/', job_detail, name='job_detail'),
    path('<int:job_id>/apply/', apply_job, name='apply_job'),
    path('<int:id>/edit/', job_edit, name='edit_job'),
    path('delete/', job_delete, name='delete_job'),
    path('search/', search_view, name="search"),
    path('filter/', filter_view, name="filter_view"),
    path('recommed/',main,name="main")

]