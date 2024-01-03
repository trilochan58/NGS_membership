import os
import requests
import json
import uuid
from datetime import datetime
from pprint import pprint

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import get_template

from paypal.standard.forms import PayPalPaymentsForm

from config.helpers import currency_rates
from accounts.models import CustomUser
from accounts.tasks import send_group_mail

from .forms import (
    InstitutionalMembershipForm,
    GeneralAndLifetimeMembershipForm,
    PaymentForm,
    VerificationForm,
    InstitutionalMembershipEditForm,
    GeneralAndLifetimeMembershipEditForm,
    RejectMembershipForm,
    StudentMembershipForm,
    EmailForm,
    CreateGroupForm
)
from .models import InstitutionalMembership, GeneralAndLifetimeMembership, Payment, StoreMail, CreateGroups
from .decorators import only_verified_users_without_any_membership, admin_only
from . import choices


@login_required
def dashboard(request):
    user = request.user
    try:
        gl_user_membership = user.general_and_lifetime_user
    except AttributeError:
        gl_user_membership = None

    try:
        ins_user_membership = user.institutional_user
    except AttributeError:
        ins_user_membership = None

    context = {
        "gl_user_membership": gl_user_membership,
        "ins_user_membership": ins_user_membership,
    }
    return render(request, "mainapp/dashboard.html", context)


@only_verified_users_without_any_membership
def new_membership_page(request):
    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    student_level = choices.STUDENT_LEVEL_CHOICES
    salutation = choices.SALUTATION_CHOICES
    districts = choices.DISTRICT_CHOICES

    if request.method == "POST":
        form_name = request.POST.get("form_name")

        if form_name == "general_membership_form":
            form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
            if form.is_valid():
                GeneralAndLifetimeMembership.objects.create(
                    created_by=request.user, membership_type="G", **form.cleaned_data
                )
                return redirect("payment")
            else:
                messages.error(
                    request, "Form not saved!!!. Please fill all the fields correctly."
                )
                general_context = {
                    "gender": gender,
                    "countries": countries,
                    "student_level": student_level,
                    "salutation": salutation,
                    "districts": districts,
                    "form": form,
                }
                return render(request, "mainapp/new-member.html", general_context)

        elif form_name == "lifetime_membership_form":
            form = GeneralAndLifetimeMembershipForm(request.POST, request.FILES)
            if form.is_valid():
                GeneralAndLifetimeMembership.objects.create(
                    created_by=request.user, membership_type="L", **form.cleaned_data
                )
                return redirect("payment")
            else:
                print(form.errors)
                messages.error(
                    request, "Form not saved!!!. Please fill all the fields correctly."
                )
                lifetime_context = {
                    "gender": gender,
                    "countries": countries,
                    "student_level": student_level,
                    "salutation": salutation,
                    "districts": districts,
                    "form": form,
                }
                return render(request, "mainapp/new-member.html", lifetime_context)

        elif form_name == "student_membership_form":
            form = StudentMembershipForm(request.POST, request.FILES)
            if form.is_valid():
                GeneralAndLifetimeMembership.objects.create(
                    created_by=request.user, membership_type="S", **form.cleaned_data
                )
                return redirect("payment")
            else:
                messages.error(
                    request, "Form not saved!!!. Please fill all the fields correctly."
                )
                student_context = {
                    "gender": gender,
                    "countries": countries,
                    "student_level": student_level,
                    "salutation": salutation,
                    "districts": districts,
                    "form": form,
                }
                return render(request, "mainapp/new-member.html", student_context)

        elif form_name == "institutional_membership_form":
            form = InstitutionalMembershipForm(request.POST, request.FILES)
            if form.is_valid():
                InstitutionalMembership.objects.create(
                    created_by=request.user, **form.cleaned_data
                )
                return redirect("institutional_payment")
            else:
                print(form.errors)
                messages.error(
                    request, "Form not saved!!!. Please fill all the fields correctly."
                )
                return render(request, "mainapp/new-member.html", {"form": form})

    context = {
        "gender": gender,
        "countries": countries,
        "student_level": student_level,
        "salutation": salutation,
        "districts": districts,
    }
    return render(request, "mainapp/new-member.html", context)


@login_required
def payment_page(request):
    """Handles the payment for individual users."""
    host = request.get_host()
    try:
        if request.user.payment_user:
            return redirect("dashboard")
    except:
        pass

    uid = uuid.uuid4()
    khalti_return_url = "https://oms.kantipurinfotech.com.np/payment-verification/"
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
        
    # paypal urls
    notify_url = f"http://{host}/paypal-ipn/"
    return_url = f"http://{host}/paypal-success-page/"
    cancel_url = f"http://{host}/payment-failed/"

    if request.user.general_and_lifetime_user.membership_type == "G":
        paypal_general_checkout = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": currency_rates(2000),
            "item_name": "general membership",
            "invoice": uid,
            "currency_code": "USD",
            "notify_url": notify_url,
            "return_url": return_url,
            "cancel_url": cancel_url,
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_general_checkout)
        context = {
            "return_url": khalti_return_url,
            "uid": uid,
            "paypal": paypal_payment,
        }
        return render(request, "mainapp/general_payment.html", context)
    elif request.user.general_and_lifetime_user.membership_type == "L":
        paypal_lifetime_checkout = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": currency_rates(10000),
            "item_name": "lifetime membership",
            "invoice": uid,
            "currency_code": "USD",
            "notify_url": notify_url,
            "return_url": return_url,
            "cancel_url": cancel_url,
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_lifetime_checkout)
        context = {
            "return_url": khalti_return_url,
            "uid": uid,
            "paypal": paypal_payment,
        }
        return render(request, "mainapp/lifetime_payment.html", context)
    elif request.user.general_and_lifetime_user.membership_type == "S":
        paypal_student_checkout = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": currency_rates(1000),
            "item_name": "student membership",
            "invoice": uid,
            "currency_code": "USD",
            "notify_url": notify_url,
            "return_url": return_url,
            "cancel_url": cancel_url,
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_student_checkout)
        context = {
            "return_url": khalti_return_url,
            "uid": uid,
            "paypal": paypal_payment,
        }
        return render(request, "mainapp/student_payment.html", context)
    else:
        return HttpResponse("dashboard")


@login_required
def institutional_payment_page(request):
    """Handles the payment for institutional users."""

    try:
        if not request.user.institutional_user:
            return redirect("dashboard")
    except:
        pass

    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)

        if form.is_valid():
            Payment.objects.create(
                user=request.user, created_at=datetime.now(), **form.cleaned_data
            )
            return redirect("payment_done_page")
        else:
            messages.error(
                request, "Process Failed!!. Submit Screenshot of your payment."
            )
    else:
        form = PaymentForm()
    return render(request, "mainapp/institutional_payment.html")


@admin_only
def general_and_lifetime_membership_verification_list(request):
    members_for_verification = GeneralAndLifetimeMembership.objects.all().order_by(
        "-id"
    )
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/gl_membership_list.html", context)


@admin_only
def general_and_lifetime_membership_verification_page(request, id):
    """Detail Page of General and Lifetime Membership to be viewed by admin."""

    general_or_lifetime_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    try:
        latest_membership_no = (
            GeneralAndLifetimeMembership.objects.filter(verification=True)
            .latest("created_at")
            .membership_no
        )
    except GeneralAndLifetimeMembership.DoesNotExist:
        latest_membership_no = "There is no membership number."

    context = {
        "gl": general_or_lifetime_object,
        "latest_membership_no": latest_membership_no,
    }
    if general_or_lifetime_object.membership_type == "S":
        return render(request, "mainapp/student_verification_page.html", context)
    else:
        return render(request, "mainapp/gl-verification-page.html", context)


@admin_only
def verify_general_or_lifetime_membership(request, id):
    verify_object = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    if request.method == "POST":
        form = VerificationForm(request.POST)
        if form.is_valid():
            membership_no = form.cleaned_data.get("membership_no")
            membership_since = form.cleaned_data.get("membership_since")

            verify_object.membership_no = membership_no
            verify_object.membership_since = membership_since
            verify_object.verification = True
            verify_object.verified_date = datetime.now()
            verify_object.save()
            messages.success(request, "Membership Verified")
            return redirect("gl_verification_list")
        else:
            messages.error(
                request,
                "Enter membership number and membership year to verify the member",
            )
            return redirect("gl_verification_page", id=verify_object.id)


@admin_only
def institutional_membership_verification_list(request):
    members_for_verification = InstitutionalMembership.objects.all().order_by("-id")
    context = {"members_for_verification": members_for_verification}
    return render(request, "mainapp/ins_membership_list.html", context)


@admin_only
def institutional_membership_verification_page(request, id):
    """Detail Page of Institutional Membership to be viewed by admin."""

    institution_object = get_object_or_404(InstitutionalMembership, id=id)
    context = {"ins": institution_object}
    return render(request, "mainapp/ins-verification-page.html", context)


@admin_only
def verify_institution_membership(request, id):
    verify_object = get_object_or_404(InstitutionalMembership, id=id)
    verify_object.verification = True
    verify_object.verified_date = datetime.now()
    verify_object.save()
    messages.success(request, "Membership Verified")
    return redirect("ins_verification_list")


@login_required
def edit_institutional_membership(request, id):
    """
    Let users edit or update their institutional membership details if they are rejected
    by admin.
    """
    instance = get_object_or_404(InstitutionalMembership, id=id)
    user = request.user

    if user.role == "U" and user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.role == "U":
        if user.institutional_user.rejected == False:
            return redirect("no_remarks")

    if request.method == "POST":
        form = InstitutionalMembershipEditForm(
            request.POST, request.FILES, instance=instance
        )
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            messages.error(request, "Please fill the form with correct data")

    context = {"ins": instance}
    return render(request, "mainapp/edit-ins-membership.html", context)


@login_required
def edit_gl_membership(request, id):
    """
    Let users edit or update their general or lifetime membership details if they are
    rejected by admin.
    """

    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    salutation = choices.SALUTATION_CHOICES
    districts = choices.DISTRICT_CHOICES
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    user = request.user

    if user.role == "U" and user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.role == "U":
        if user.general_and_lifetime_user.rejected == False:
            return redirect("no_remarks")

    if request.method == "POST":
        form = GeneralAndLifetimeMembershipEditForm(
            request.POST, request.FILES, instance=instance
        )
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            pprint(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = GeneralAndLifetimeMembershipEditForm(instance=instance)
    context = {"gl": instance, "gender": gender, "countries": countries, "salutation": salutation, "districts": districts}
    return render(request, "mainapp/edit-gl-membership.html", context)


@admin_only
def reject_instutional_membership(request, id):
    instance = get_object_or_404(InstitutionalMembership, id=id)

    if request.method == "POST":
        form = RejectMembershipForm(request.POST)
        if form.is_valid():
            instance.remarks = form.cleaned_data.get("remarks")
            instance.rejected = True
            instance.save()
            return redirect("ins_verification_list")


@admin_only
def reject_gl_membership(request, id):
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)

    if request.method == "POST":
        form = RejectMembershipForm(request.POST)
        if form.is_valid():
            instance.remarks = form.cleaned_data.get("remarks")
            instance.rejected = True
            instance.save()
            return redirect("gl_verification_list")


@login_required
def remarks(request):
    """
    If admin rejects and sends remarks then acc to membership_type of user it redirects
    to correct edit page.
    """
    user = request.user
    try:
        gl_or_ins = GeneralAndLifetimeMembership.objects.get(created_by_id=user.id)
        if gl_or_ins.be_subject:
            return redirect("edit_gl_membership", id=gl_or_ins.id)
        else:
            return redirect("edit_student_membership", id=gl_or_ins.id)
    except:
        gl_or_ins = InstitutionalMembership.objects.get(created_by_id=user.id)
        return redirect("edit_ins_membership", id=gl_or_ins.id)


@login_required
def no_remarks(request):
    return render(request, "mainapp/remarks.html")


@login_required
def upgrade_to_lifetime(request):
    return render(request, "mainapp/upgrade_to_lifetime.html")


@login_required
def edit_student_membership(request, id):
    """
    Let users edit or update their student membership details if they are rejected by
    admin.
    """

    gender = choices.GENDER_CHOICES
    countries = choices.COUNTRY_CHOICES
    student_level = choices.STUDENT_LEVEL_CHOICES
    instance = get_object_or_404(GeneralAndLifetimeMembership, id=id)
    user = request.user

    if user.id != instance.created_by.id:
        return redirect("dashboard")

    if user.general_and_lifetime_user.rejected == False:
        return redirect("no_remarks")

    if request.method == "POST":
        form = StudentMembershipForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.rejected = False
            form_instance.save()
            messages.success(request, "Details Updated")
            return redirect("dashboard")
        else:
            pprint(form.errors)
            messages.error(request, "Please fill the form with correct data")
    else:
        form = StudentMembershipForm(instance=instance)
    context = {
        "gl": instance,
        "gender": gender,
        "countries": countries,
        "student_level": student_level,
    }
    return render(request, "mainapp/edit_student_membership.html", context)


@login_required
def payment_done_page(request):
    return render(request, "mainapp/payment-success.html")


@login_required
def payment_failed_page(request):
    return render(request, "mainapp/payment-failed.html")


def initiate_khalti(request):
    """Initiates the payment by user and redirects them to the payment url."""
    user = request.user
    purchase_order_id = request.POST.get("purchase_order_id")
    amount = request.POST.get("amount")
    return_url = request.POST.get("return_url")

    url = "https://khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps(
        {
            "return_url": return_url,
            "website_url": "https://example.com/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
            },
        }
    )
    headers = {
        "Authorization": os.getenv("khalti_live_secret_key"),
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    pprint(new_res)

    if response.status_code == 200:
        return redirect(new_res["payment_url"])
    else:
        messages.error(
            request, "Payment failed. Check your phone number and other details."
        )
        return redirect("payment")


def payment_verification(request):
    """Verifies the users payment done in khalti."""
    pidx = request.GET.get("pidx")
    amount = request.GET.get("amount")
    txn_id = request.GET.get("txnId")

    url = "https://khalti.com/api/v2/epayment/lookup/"
    headers = {
        "Authorization": os.getenv("khalti_live_secret_key"),
        "Content-Type": "application/json",
    }
    payload = json.dumps({"pidx": pidx})
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    if response.json()["status"] == "Completed":
        Payment.objects.create(
            created_at=datetime.now(),
            user_id=request.user.id,
            paid_amount_in_paisa=amount,
            pidx=pidx,
            txn_id=txn_id,
        )
        messages.success(request, "Payment Successful")
        return redirect("payment_done_page")
    else:
        # message = request.GET.get("message")
        return redirect("payment_failed")


def paypal_success_page(request):
    """Users are redirected here if payment is successful in paypal."""
    payer_id = request.GET.get("PayerID")
    Payment.objects.create(
        created_at=datetime.now(),
        user_id=request.user.id,
        paypal_payer_id=payer_id,
    )
    messages.success(request, "Payment Successful")
    return redirect("payment_done_page")


@admin_only
def group_mail(request):
    """Sends mail in groups."""
    custom_groups = CreateGroups.objects.all()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            group = request.POST.getlist("group")
            if not group:
                messages.error(request, "Please select a group to send mail!")
                return render(request, "mainapp/send_mail.html", {"form": form})
            
            #Initialized empty list for storing emails
            mail_lists = []
            if "lifetime" in group:
                lifetime_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="L", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for lifetime_mail in lifetime_mails:
                    mail_lists.append(lifetime_mail)
            if "general" in group:
                general_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="G", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for general_mail in general_mails:
                    mail_lists.append(general_mail)
            if "student" in group:
                student_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="S", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for student_mail in student_mails:
                    mail_lists.append(student_mail)
            if "institutional" in group:
                institutional_mails = InstitutionalMembership.objects.filter(verification=True).values_list("created_by__email", flat=True)
                for institutional_mail in institutional_mails:
                    mail_lists.append(institutional_mail)
            for custom_group in custom_groups:
                if custom_group.name in group:
                    for user in custom_group.custom_users.all():
                        mail_lists.append(user.email)
                        
            #Removes duplicate emails in case they exist
            unique_email_list = list(set(mail_lists))
            # print(unique_email_list)
            custom_users = CustomUser.objects.filter(email__in=unique_email_list)
            store_mail_instance = StoreMail.objects.create(subject=subject, message=message)
            store_mail_instance.groups_mail.add(*custom_users)
            store_mail_instance.set_associated_groups(group)
            
            if "send" in request.POST:
                store_mail_instance.mail_status = "S"
                store_mail_instance.save()
                send_group_mail(subject, message, unique_email_list)
                messages.success(request, "Mail Sent to Group.")
                return redirect("mail_lists")
            elif "draft" in request.POST:
                store_mail_instance.mail_status = "D"
                store_mail_instance.save()
                messages.success(request, "Mail Saved as Draft.")
                return redirect("mail_lists")
        else:
            messages.error(request, "Please enter the subject and message correctly.")
            return render(request, "mainapp/send_mail.html", {"form": form})
    else:
        form = EmailForm()
    context = {"groups": custom_groups}
    return render(request, "mainapp/send_mail.html", context)


@admin_only
def create_group(request):
    """Lets admin create custom groups by associating verified users."""
    custom_users = CustomUser.objects.filter(is_verified=True)
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            users = request.POST.getlist("users")
            if name in ["lifetime", "general", "student", "institutional"]:
                messages.error(request, "Group name cannot be one of these: lifetime, general, student, institutional")
                return render(request, "mainapp/create-group.html", {"form": form})
            if CreateGroups.objects.filter(name=name).exists():
                messages.error(request, "Group with this name already exists! Enter another unique group name.")
                return render(request, "mainapp/create-group.html", {"form": form})
            if not users:
                messages.error(request, "Please select users to create group!")
                return render(request, "mainapp/create-group.html", {"form": form})
            create_group_instance = CreateGroups.objects.create(name=name, description=description)
            create_group_instance.custom_users.add(*users)
            create_group_instance.save()
            messages.success(request, "Group created successfully.")
            return redirect("group_lists")
        else:
            messages.error(request, "Please enter the details correctly.")
            return render(request, "mainapp/create-group.html", {"form": form})
    else:
        form = CreateGroupForm()
    context = {"users": custom_users}
    return render(request, "mainapp/create-group.html", context)


@login_required
def view_gl_or_ins_details(request):
    """To let users see their membership details."""
    
    gl_instance = None
    ins_instance = None
    
    try:
        gl_instance = GeneralAndLifetimeMembership.objects.get(created_by=request.user)
    except GeneralAndLifetimeMembership.DoesNotExist:
        pass
    try:
        ins_instance = InstitutionalMembership.objects.get(created_by=request.user)
    except InstitutionalMembership.DoesNotExist:
        pass

    context = {"gl": gl_instance, "ins": ins_instance}
    if gl_instance:
        if gl_instance.be_subject:
            return render(request, "mainapp/view_gl_details.html", context)
        elif gl_instance.level:
            return render(request, "mainapp/view_student_details.html", context)
    elif ins_instance:
        return render(request, "mainapp/view_ins_details.html", context)


@admin_only
def group_mail_list(request):
    stored_mails = StoreMail.objects.all()
    context = {"mails": stored_mails}
    return render(request, "mainapp/mail_list.html", context)


@admin_only
def group_list(request):
    custom_groups = CreateGroups.objects.all()
    context = {"groups": custom_groups}
    return render(request, "mainapp/group_list.html", context)


@admin_only
def edit_groups(request, id):
    custom_users = CustomUser.objects.filter(is_verified=True)
    group_instance = CreateGroups.objects.get(id=id)
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            users = request.POST.getlist("users")
            print(name)
            print(description)
            print(users)
            if name in ["lifetime", "general", "student", "institutional"]:
                messages.error(request, "Group name cannot be one of these: lifetime, general, student, institutional")
                return redirect("edit_group", id=group_instance.id)
            if CreateGroups.objects.exclude(name=group_instance.name).filter(name=name).exists():
                messages.error(request, "Group with this name already exists! Enter another unique group name.")
                return redirect("edit_group", id=group_instance.id)
            if not users:
                messages.error(request, "Please select users to create group!")
                return redirect("edit_group", id=group_instance.id)
            group_instance.name = name
            group_instance.description = description
            group_instance.custom_users.set(users)
            group_instance.save()
            messages.success(request, "Group Updated")
            return redirect("group_lists")
        else:
            messages.error(request, "Fill form correctly")
            # return render(request, "mainapp/edit_groups.html", {"form": form}) 

    context = {"group": group_instance, "users": custom_users}
    return render(request, "mainapp/edit_groups.html", context)


@admin_only
def edit_stored_mail(request, id):
    custom_groups = CreateGroups.objects.all()
    mail_instance = StoreMail.objects.get(id=id)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            group = request.POST.getlist("group")
            print(subject)
            print(message)
            print(group)
            if not group:
                messages.error(request, "Please select a group to send mail!")
                return redirect("edit_mail", id=id)
            
            #Initialized empty list for storing emails
            mail_lists = []
            if "lifetime" in group:
                lifetime_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="L", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for lifetime_mail in lifetime_mails:
                    mail_lists.append(lifetime_mail)
            if "general" in group:
                general_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="G", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for general_mail in general_mails:
                    mail_lists.append(general_mail)
            if "student" in group:
                student_mails = CustomUser.objects.filter(general_and_lifetime_user__membership_type="S", general_and_lifetime_user__verification=True).values_list("email", flat=True)
                for student_mail in student_mails:
                    mail_lists.append(student_mail)
            if "institutional" in group:
                institutional_mails = InstitutionalMembership.objects.filter(verification=True).values_list("created_by__email", flat=True)
                for institutional_mail in institutional_mails:
                    mail_lists.append(institutional_mail)
            for custom_group in custom_groups:
                if custom_group.name in group:
                    for user in custom_group.custom_users.all():
                        mail_lists.append(user.email)
            #Removes duplicate emails in case they exist
            unique_email_list = list(set(mail_lists))
            users = CustomUser.objects.filter(email__in=unique_email_list)
            mail_instance.subject = subject
            mail_instance.message = message
            mail_instance.groups_mail.set(users)
            mail_instance.set_associated_groups(group)
            
            if "send" in request.POST:
                mail_instance.mail_status = "S"
                mail_instance.save()
                send_group_mail(subject, message, unique_email_list)
                messages.success(request, "Mail Sent to Group.")
                return redirect("mail_lists")
            elif "draft" in request.POST:
                mail_instance.mail_status = "D"
                mail_instance.save()
                messages.success(request, "Mail Saved as Draft.")
                return redirect("mail_lists")
        else:
            messages.error(request, "Please enter the subject and message correctly.")
            return redirect("edit_mail", id=id)
    else:
        form = EmailForm()
    context = {"mail": mail_instance, "groups": custom_groups}
    return render(request, "mainapp/edit_mail.html", context)