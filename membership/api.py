from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment
from django.http import JsonResponse
from django.core.serializers import serialize


def membership_api(request, id):
    host = request.get_host()
    membership_instance = GeneralAndLifetimeMembership.objects.get(id=id)
    
    try:
        payment_instance = Payment.objects.get(user=membership_instance.created_by)
    except Payment.DoesNotExist:
        payment_instance = None
    
    payment_created_at = payment_instance.created_at if payment_instance else None
    payment_ss = f"http://{host}{payment_instance.payment_ss.url}" if payment_instance else None
    amount = payment_instance.amount_in_rs if payment_instance else None
    paypal_id = payment_instance.paypal_payer_id if payment_instance else None
    college_id_card = f"http://{host}{membership_instance.college_id_card.url}" if membership_instance.college_id_card else None
    
    
    if payment_instance:
        payment_status = True
    else:
        payment_status = False
    
    
    serialized_data = {
        "name_of_applicant": membership_instance.name_of_applicant,
        "dob": membership_instance.dob,
        "gender": membership_instance.get_gender_display(),
        "permanent_address": membership_instance.permanent_address,
        "affiliation": membership_instance.affiliation,
        "nationality": membership_instance.get_nationality_display(),
        "citizenship_no": membership_instance.citizenship_card_no,
        "issued_from": membership_instance.get_issued_from_display(),
        "be_subject": membership_instance.be_subject,
        "be_institution": membership_instance.be_institution,
        "be_country": membership_instance.get_be_country_display(),
        "be_passed_year": membership_instance.be_passed_year,
        "me_subject": membership_instance.me_subject,
        "me_institution": membership_instance.me_institution,
        "me_country": membership_instance.get_me_country_display(),
        "me_passed_year": membership_instance.me_passed_year,
        "phd_subject": membership_instance.phd_subject,
        "phd_institution": membership_instance.phd_institution,
        "phd_country": membership_instance.get_phd_country_display(),
        "phd_passed_year": membership_instance.phd_passed_year,
        "work_experience": membership_instance.work_experience,
        "pp_photo": f"http://{host}{membership_instance.pp_photo.url}",
        "citizenship_photo": f"http://{host}{membership_instance.citizenship.url}",
        "masters_document": f"http://{host}{membership_instance.masters_document.url}",
    
        #ayment details
        "payment_status": payment_status,
        "payment_created_at": payment_created_at,
        "payment_ss": payment_ss,
        "amount": amount,
        "paypal_id": paypal_id,
    }
    return JsonResponse(serialized_data, safe=False)


def institutional_membership_api(request, id):
    host = request.get_host()
    membership_instance = InstitutionalMembership.objects.get(id=id)
    
    try:
        payment_instance = Payment.objects.get(user=membership_instance.created_by)
    except Payment.DoesNotExist:
        payment_instance = None

    payment_created_at = payment_instance.created_at if payment_instance else None
    payment_ss = f"http://{host}{payment_instance.payment_ss.url}" if payment_instance else None
    amount = payment_instance.amount_in_rs if payment_instance else None
    paypal_id = payment_instance.paypal_payer_id if payment_instance else None
    
    if payment_instance:
        payment_status = True
    else:
        payment_status = False
        
    serialized_data = {
        "company_name": membership_instance.company_name,
        "company_address": membership_instance.company_name,
        "registration_no": membership_instance.registration_no,
        "working_field": membership_instance.working_field,
        "contact_person": membership_instance.contact_person,
        "contact_number": membership_instance.contact_number,
        "website": membership_instance.website,
        "logo": f"http://{host}{membership_instance.logo.url}",
        "pan_document": f"http://{host}{membership_instance.pan_document.url}",
        "registration_document": f"http://{host}{membership_instance.registration_document.url}",
        "company_document": f"http://{host}{membership_instance.company_document.url}",
        
        "payment_status": payment_status,
        "payment_created_at": payment_created_at,
        "payment_ss": payment_ss,
        "amount": amount,
        "paypal_id": paypal_id,
    }
    return JsonResponse(serialized_data, safe=False)


def student_membership_api(request, id):
    host = request.get_host()
    membership_instance = GeneralAndLifetimeMembership.objects.get(id=id)
    
    try:
        payment_instance = Payment.objects.get(user=membership_instance.created_by)
    except Payment.DoesNotExist:
        payment_instance = None
    
    payment_created_at = payment_instance.created_at if payment_instance else None
    payment_ss = f"http://{host}{payment_instance.payment_ss.url}" if payment_instance else None
    amount = payment_instance.amount_in_rs if payment_instance else None
    paypal_id = payment_instance.paypal_payer_id if payment_instance else None
    # college_id_card = f"http://{host}{membership_instance.college_id_card.url}" if membership_instance.college_id_card else None
    
    
    if payment_instance:
        payment_status = True
    else:
        payment_status = False
    
    
    serialized_data = {
        "salutation"
        "name_of_applicant": membership_instance.name_of_applicant,
        "dob": membership_instance.dob,
        "gender": membership_instance.get_gender_display(),
        "permanent_address": membership_instance.permanent_address,
        "affiliation": membership_instance.affiliation,
        "nationality": membership_instance.get_nationality_display(),
        "citizenship_no": membership_instance.citizenship_card_no,
        "issued_from": membership_instance.get_issued_from_display(),
        "level": membership_instance.get_level_display(),
        "institution": membership_instance.institution,
        "country_of_institution": membership_instance.get_country_of_institution_display(),
        "expected_pass_year": membership_instance.expected_pass_year,
        "work_experience": membership_instance.work_experience,
        "pp_photo": f"http://{host}{membership_instance.pp_photo.url}",
        "citizenship_photo": f"http://{host}{membership_instance.citizenship.url}",
        "college_id_card": f"http://{host}{membership_instance.college_id_card.url}",
        
        #ayment details
        "payment_status": payment_status,
        "payment_created_at": payment_created_at,
        "payment_ss": payment_ss,
        "amount": amount,
        "paypal_id": paypal_id,
    }
    return JsonResponse(serialized_data, safe=False)