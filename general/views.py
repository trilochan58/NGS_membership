from django.shortcuts import render

from membership.models import GeneralAndLifetimeMembership, InstitutionalMembership


def homepage(request):
    return render(request, "general/index.html")


def guidelines(request):
    return render(request, "general/guidelines.html")


def gl_general_list(request):
    gl_members = GeneralAndLifetimeMembership.objects.filter(
        verification=True, membership_type__in=["G", "L"]
    )
    context = {"gl_members": gl_members}
    return render(request, "general/general-member-list.html", context)


def ins_general_list(request):
    ins_members = InstitutionalMembership.objects.filter(verification=True)
    context = {"ins_members": ins_members}
    return render(request, "general/institutional-member-list.html", context)


def student_general_list(request):
    student_members = GeneralAndLifetimeMembership.objects.filter(
        verification=True, membership_type="S"
    )
    context = {"student_members": student_members}
    return render(request, "general/student-member.html", context)
