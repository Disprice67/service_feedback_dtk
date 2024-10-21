from . import views
from django.urls import path

app_name = 'activity'

urlpatterns = [
    path('', views.index, name='index'),
    path('sending/activity/', views.index, name='sending_activity'),
    path('sending/activity/managers/<int:active_id>/', views.managers, name='sending_managers'),
    path('sending/activity/manager/<int:active_id>/edit', views.manager_edit, name='sending_manager_edit'),
    path('activity/managers/<int:active_id>/standard_feedback/', views.standard_feedback, name='standard_feedback'),
    path('activity/managers/<int:active_id>/', views.managers, name='managers'),
    path('activity/manager/<int:active_id>>/edit', views.manager_edit, name='manager_edit'),
    path('project_file/<int:active_id>/dowload', views.download_file_project, name='dowload_file_project')
]
