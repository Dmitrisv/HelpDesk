from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.new_request, name="new"),
    path("req-delete/<int:id>/", views.complitedreq, name="delreq"),
    path("req-take/<int:id>/", views.takereq, name="takereq"),
    path("req-join/<int:id>/", views.sub_implementor, name="joinreq"),
    path("requests/", views.get_all_requests, name="requests"),
    path('tasks/', views.tasks, name="tasks"),
    path('done-task/<int:id>', views.taskdone, name="taskdone"),
    path("sign-up/", views.sign_up),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html')),
    path("request/<int:id>", views.req_info, name="request_info"),
    path("profile/",views.profile,name="profile"),
]
