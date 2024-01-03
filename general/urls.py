from django.urls import path

from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("guidelines/", views.guidelines, name="guidelines"),
    path("gl-general-list/", views.gl_general_list, name="gl_general_list"),
    path("ins-general-list/", views.ins_general_list, name="ins_general_list"),
    path(
        "student-general-list/", views.student_general_list, name="student_general_list"
    ),
]
