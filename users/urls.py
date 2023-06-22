from django.urls import path,include
from users.views import profile_view,profile_edit, application_view, view_message, application_delete
app_name = "users"


urlpatterns = [
  
    path("profile/userid = <int:id>/",profile_view, name='profile'),
    path("profile/edit/userid = <int:id>/",profile_edit, name='profileedit'),
    path("myapplications/",application_view, name='application_view'),
    path("myapplications/delete/",application_delete, name='application_delete'),
    path('myapplications/view_message/<int:id>', view_message, name="view_message"),


]