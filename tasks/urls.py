from django.urls import path
from . import views

urlpatterns = [
    # Templates (web interface)
    path("", views.tasks_api, name="index"),
    path("add/", views.tasks_api, name="add_task"),

    # API endpoints (JSON)
    path("api/tasks/", views.task_detail_api, name="api_tasks_list_create"),  # GET list, POST create
    path("api/tasks/<int:task_id>/", views.task_detail_api, name="api_task_detail"),
]