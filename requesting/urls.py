from django.urls import path

from . import views

urlpatterns = [
    path("", views.new_request, name="new"),
    path("req-delete/<int:id>/", views.complitedreq, name="delreq"),
    path("req-take/<int:id>/", views.takereq, name="takereq"),
    path("req-join/<int:id>/", views.sub_implementor, name="joinreq"),
    path("requests/", views.get_all_requests, name="requests"),
    path('tasks/',views.tasks,name="tasks"),
    path('done-task/<int:id>',views.taskdone,name="taskdone"),
    path("sign-up/", views.sign_up),
]
