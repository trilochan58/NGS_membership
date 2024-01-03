from django.contrib import admin

from .models import GeneralAndLifetimeMembership, InstitutionalMembership, Payment, StoreMail, CreateGroups


class PaymentModelAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_full_name",
        "amount_in_rs",
    )

    def get_user_full_name(self, obj):
        return obj.user.full_name

    get_user_full_name.short_description = "User Full Name"


admin.site.register(GeneralAndLifetimeMembership)
admin.site.register(InstitutionalMembership)
admin.site.register(StoreMail)
admin.site.register(CreateGroups)
admin.site.register(Payment, PaymentModelAdmin)
