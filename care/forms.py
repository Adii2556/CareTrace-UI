from pathlib import Path

from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from accounts.models import PatientProfile

from .models import (
    ALLOWED_MEDICAL_CONTENT_TYPES,
    ALLOWED_MEDICAL_EXTENSIONS,
    MedicalRecord,
    Referral,
)


class PatientChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, patient):
        profile = patient.profile
        name = patient.get_full_name() or patient.username
        return f"{name} · {profile.caretrace_id}"


class ClinicianChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, clinician):
        name = clinician.get_full_name() or clinician.username
        organization = clinician.profile.organization or "Organization not specified"
        return f"{name} · {organization}"


class ReferralCreateForm(forms.ModelForm):
    patient = PatientChoiceField(queryset=User.objects.none(), empty_label="Select patient")
    clinician = ClinicianChoiceField(
        queryset=User.objects.none(),
        label="Destination clinician",
        empty_label="Select destination clinician",
    )

    def __init__(self, *args, creator, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = creator
        self.fields["patient"].queryset = (
            User.objects.filter(profile__role=PatientProfile.Role.PATIENT)
            .filter(Q(referrals__clinician=creator) | Q(referrals__created_by=creator))
            .distinct()
            .order_by("first_name", "last_name", "username")
        )
        self.fields["clinician"].queryset = User.objects.filter(
            profile__role=PatientProfile.Role.CLINICIAN
        ).order_by("first_name", "last_name", "username")
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_clinician(self):
        clinician = self.cleaned_data["clinician"]
        if not clinician.profile.organization:
            raise forms.ValidationError(
                "The destination clinician must have an organization before referral."
            )
        return clinician

    class Meta:
        model = Referral
        fields = (
            "patient",
            "clinician",
            "specialty",
            "reason",
            "clinical_summary",
            "diagnosis",
            "priority",
            "notes",
        )
        labels = {
            "specialty": "Department or speciality",
            "reason": "Reason for referral",
            "clinical_summary": "Clinical summary",
            "diagnosis": "Relevant diagnosis",
            "notes": "Additional notes",
        }
        help_texts = {
            "patient": "Only patients already connected to your clinical account are listed.",
            "clinical_summary": "Provide only the context needed for this referral.",
            "notes": "Optional operational notes for the referral.",
        }
        widgets = {
            "specialty": forms.TextInput(attrs={"placeholder": "e.g. Cardiology"}),
            "reason": forms.TextInput(attrs={"placeholder": "Reason for specialist review"}),
            "clinical_summary": forms.Textarea(attrs={"rows": 4}),
            "diagnosis": forms.TextInput(attrs={"placeholder": "Optional"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class MedicalRecordForm(forms.ModelForm):
    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")
        if (
            uploaded_file
            and Path(uploaded_file.name).suffix.lower() not in ALLOWED_MEDICAL_EXTENSIONS
        ):
            raise forms.ValidationError("Upload a PDF, PNG, JPG, or JPEG file.")
        if uploaded_file and uploaded_file.content_type not in ALLOWED_MEDICAL_CONTENT_TYPES:
            raise forms.ValidationError(
                "The uploaded file type does not match an allowed medical document."
            )
        return uploaded_file

    class Meta:
        model = MedicalRecord
        fields = ("title", "category", "provider", "recorded_on", "summary", "file")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "provider": forms.TextInput(attrs={"class": "form-control"}),
            "recorded_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "file": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".pdf,.png,.jpg,.jpeg"}
            ),
        }
