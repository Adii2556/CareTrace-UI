from django.contrib import admin

from .models import AccessLog, Appointment, MedicalRecord, Medication, Referral


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "category", "provider", "recorded_on", "status")
    list_filter = ("category", "status", "provider")
    search_fields = ("title", "patient__username", "provider")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "patient",
        "created_by",
        "reason",
        "status",
        "receiving_provider",
    )
    list_filter = ("status", "priority", "specialty")
    search_fields = (
        "reference_id",
        "patient__username",
        "patient__first_name",
        "patient__last_name",
        "reason",
        "specialty",
    )
    filter_horizontal = ("selected_records",)


admin.site.register(Appointment)
admin.site.register(Medication)
admin.site.register(AccessLog)
