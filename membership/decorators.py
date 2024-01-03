from django.shortcuts import redirect

from .models import GeneralAndLifetimeMembership, InstitutionalMembership


def only_verified_users_without_any_membership(view_func):
    """
    If user has entered pin and verified themselves and they don't have any type of 
    membership, then only those users can access views.
    """

    def wrap(request, *args, **kwargs):
        user = request.user
        general_and_lifetime_membership_does_not_exist = not (
            GeneralAndLifetimeMembership.objects.filter(created_by=user.id).exists()
        )
        institutional_membership_does_not_exist = not (
            InstitutionalMembership.objects.filter(created_by=user.id).exists()
        )
        if (
            user.is_authenticated
            and not user.role == "A"
            and user.is_verified == True
            and general_and_lifetime_membership_does_not_exist
            and institutional_membership_does_not_exist
        ):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap


def admin_only(view_func):
    """Only allows users with role set to admin."""

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role == "A":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap


def user_login_check(view_func):
    """Restricts authenticated user from visiting the login page."""

    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")

    return wrap
