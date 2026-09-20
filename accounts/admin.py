from django.contrib import admin

from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "caretrace_id", "organization")
    list_filter = ("role",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "caretrace_id")

