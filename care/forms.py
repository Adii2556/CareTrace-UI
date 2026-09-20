from pathlib import Path

from django import forms

from .models import ALLOWED_MEDICAL_CONTENT_TYPES, ALLOWED_MEDICAL_EXTENSIONS, MedicalRecord


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
