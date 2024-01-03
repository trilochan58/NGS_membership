from django import forms

from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment


class InstitutionalMembershipForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        exclude = ["created_by", "remarks", "verified_date"]


class GeneralAndLifetimeMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        exclude = [
            "created_by",
            "membership_type",
            "remarks",
            "verified_date",
            "level",
            "institution",
            "country_of_institution",
            "expected_pass_year",
            "college_id_card",
        ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_ss"]


class InstitutionalMembershipEditForm(forms.ModelForm):
    class Meta:
        model = InstitutionalMembership
        fields = [
            "company_name",
            "company_address",
            "registration_no",
            "pan_document",
            "registration_document",
            "company_document",
            "working_field",
            "contact_person",
            "contact_number",
            "website",
            "logo",
        ]


class GeneralAndLifetimeMembershipEditForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        fields = [
            "salutation",
            "name_of_applicant",
            "dob",
            "gender",
            "nationality",
            "issued_from",
            "permanent_address",
            "affiliation",
            "citizenship_card_no",
            "be_subject",
            "be_institution",
            "be_country",
            "be_passed_year",
            "me_subject",
            "me_institution",
            "me_country",
            "me_passed_year",
            "phd_subject",
            "phd_institution",
            "phd_country",
            "phd_passed_year",
            "pp_photo",
            "citizenship",
            "masters_document",
            "work_experience",
        ]


class VerificationForm(forms.Form):
    membership_no = forms.CharField()
    membership_since = forms.CharField(max_length=4)


class RejectMembershipForm(forms.Form):
    remarks = forms.CharField(required=True)


class StudentMembershipForm(forms.ModelForm):
    class Meta:
        model = GeneralAndLifetimeMembership
        fields = [
            "salutation",
            "name_of_applicant",
            "dob",
            "gender",
            "nationality",
            "issued_from",
            "permanent_address",
            "affiliation",
            "citizenship_card_no",
            "pp_photo",
            "citizenship",
            "college_id_card",
            "level",
            "institution",
            "country_of_institution",
            "expected_pass_year",
        ]


class EmailForm(forms.Form):
    """Form for handling email details while sending group mails."""
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class CreateGroupForm(forms.Form):
    """Form for handling group creation."""
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)