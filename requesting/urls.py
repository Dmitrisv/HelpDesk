from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .views import HistoryListView, PublicProfileView

urlpatterns = [
    path("", views.new_request, name="new"),
    path("req-delete/<int:id>/", views.complitedreq, name="delreq"),
    path("req-take/<int:id>/", views.takereq, name="takereq"),
    path("req-join/<int:id>/", views.sub_implementor, name="joinreq"),
    path("requests/", views.get_all_requests, name="requests"),
    path("tasks/", views.tasks, name="tasks"),
    path("done-task/<int:id>", views.taskdone, name="taskdone"),
    path("sign-up/", views.sign_up, name="sing_up"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            html_email_template_name="registration/password_reset_email.html"
        ),
        name="reset_password",
    ),
    path("request/<int:id>", views.req_info, name="request_info"),
    path("profile/", views.profile, name="profile"),
    path(
        "settings/profile/",
        PublicProfileView.as_view(),
        name="profile_settings",
    ),
    path("settings/security/", views.change_password, name="security_settings"),
    path(
        "settings/appearance/", views.set_appearance, name="appearance_settings"
    ),
    path("history/", HistoryListView.as_view(), name="history"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("article/<slug:article_slug>/", views.get_article, name="article"),
    path("article/", views.articles, name="articles"),
]
