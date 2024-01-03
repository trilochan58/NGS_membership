from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("change-password/", views.change_password, name="change_password"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("verify-user/", views.verify_user, name="verify_user"),
    # url paths for password resetting
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(
            template_name="auth/forget-password.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/reset-password.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
