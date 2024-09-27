from django.urls import path

from core.dashboard.auth import sign_in, sign_out, user_profile, manage_user, change_password

from core.dashboard.task import manage_task, task_filter
from core.dashboard.view import index

urlpatterns = [
    # auth
    path('', index, name="home"),
    path('login/', sign_in, name="login"),
    path('logout/', sign_out, name="logout"),
    path('user-profile/<int:user_id>/', user_profile, name="user-profile"),

    # users
    path("users/<int:ut>/", manage_user, name="users"),
    path("users/<int:ut>/add/<status>/", manage_user, name="users-add"),
    path("users/<int:ut>/edit/<status>/<int:pk>/", manage_user, name="users-edit"),
    path("users/chp/<int:user_id>/", change_password, name="users-chp"),

    # task
    path("task/", manage_task, name="task"),
    path("task/form/<status>/", manage_task, name="task-add"),
    path("task/edit/<status>/<int:pk>/", manage_task, name="task-edit"),
    path("task/del/<int:delete>/<int:pk>/", manage_task, name="task-del"),
    path("task/filter/<key>/<int:pk>/", task_filter, name="task-filter"),


]
