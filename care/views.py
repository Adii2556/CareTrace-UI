from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import PatientProfile
from ai_services.services import AIServiceUnavailable, explain_medical_record

from .decorators import role_required
from .forms import MedicalRecordForm
from .models import AccessLog, MedicalRecord, Referral


def healthcheck(request):
    return JsonResponse({"status": "ok", "service": "caretrace"})


def home(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == PatientProfile.Role.CLINICIAN:
        referral = request.user.assigned_referrals.first()
        if referral:
            if referral.status == Referral.Status.PENDING:
                return redirect("care:select_records", referral_id=referral.id)
            return redirect("care:doctor_workspace", referral_id=referral.id)
    return redirect("care:dashboard")


def _patient_referral(user, referral_id):
    return get_object_or_404(
        Referral.objects.prefetch_related("selected_records"),
        id=referral_id,
        patient=user,
    )


@role_required(PatientProfile.Role.PATIENT)
def dashboard(request):
    patient = request.user
    pending_referral = patient.referrals.filter(status=Referral.Status.PENDING).first()
    latest_referral = patient.referrals.first()
    upcoming = patient.appointments.filter(status="scheduled").first()
    active_medication = patient.medications.filter(active=True).first()
    pending_test = patient.medical_records.filter(status=MedicalRecord.Status.PENDING).first()
    latest_result = patient.medical_records.filter(
        status=MedicalRecord.Status.AVAILABLE, category=MedicalRecord.Category.LAB
    ).first()

    recent_activity = []
    if latest_referral:
        recent_activity.append(
            {
                "title": f"{latest_referral.reason.replace(' Evaluation', '')} Referral",
                "summary": latest_referral.get_status_display(),
                "date": latest_referral.requested_at.date(),
                "icon": "Route",
            }
        )
    recent_activity.extend(
        {
            "title": record.title,
            "summary": record.summary or f"{record.get_status_display()} · {record.provider}",
            "date": record.recorded_on,
            "icon": record.icon_name,
        }
        for record in patient.medical_records.filter(status=MedicalRecord.Status.AVAILABLE)[:4]
    )
    recent_activity.sort(key=lambda item: item["date"], reverse=True)

    return render(
        request,
        "care/dashboard.html",
        {
            "active_nav": "dashboard",
            "pending_referral": pending_referral,
            "latest_referral": latest_referral,
            "upcoming": upcoming,
            "active_medication": active_medication,
            "pending_test": pending_test,
            "latest_result": latest_result,
            "recent_activity": recent_activity[:5],
        },
    )


@role_required(PatientProfile.Role.PATIENT)
def timeline(request):
    query = request.GET.get("q", "").strip()
    records_qs = request.user.medical_records.all()
    if query:
        records_qs = records_qs.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(provider__icontains=query)
        )
    return render(
        request,
        "care/timeline.html",
        {
            "active_nav": "timeline",
            "records": records_qs,
            "query": query,
            "referral": request.user.referrals.first(),
        },
    )


@role_required(PatientProfile.Role.PATIENT)
def records(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    provider = request.GET.get("provider", "").strip()
    records_qs = request.user.medical_records.all()
    if query:
        records_qs = records_qs.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(provider__icontains=query)
        )
    if category:
        records_qs = records_qs.filter(category=category)
    if provider:
        records_qs = records_qs.filter(provider=provider)
    providers = (
        request.user.medical_records.order_by("provider")
        .values_list("provider", flat=True)
        .distinct()
    )
    return render(
        request,
        "care/records.html",
        {
            "active_nav": "records",
            "records": records_qs,
            "query": query,
            "category": category,
            "provider": provider,
            "providers": providers,
            "categories": MedicalRecord.Category.choices,
            "record_form": MedicalRecordForm(),
        },
    )


@role_required(PatientProfile.Role.PATIENT)
@require_POST
def add_record(request):
    form = MedicalRecordForm(request.POST, request.FILES)
    if form.is_valid():
        record = form.save(commit=False)
        record.patient = request.user
        record.save()
        messages.success(request, "Medical record added securely.")
    else:
        error_text = " ".join(
            str(message) for errors in form.errors.values() for message in errors
        )
        messages.error(request, error_text or "Please correct the record details.")
    return redirect("care:records")


@login_required
def download_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    is_owner = record.patient_id == request.user.id
    profile = getattr(request.user, "profile", None)
    is_authorized_clinician = bool(
        profile
        and profile.role == PatientProfile.Role.CLINICIAN
        and record.referrals.filter(clinician=request.user).exclude(
            status__in=[Referral.Status.PENDING, Referral.Status.REJECTED]
        ).exists()
    )
    if not (is_owner or is_authorized_clinician) or not record.file:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    return FileResponse(
        record.file.open("rb"),
        as_attachment=True,
        filename=Path(record.file.name).name,
    )


@role_required(PatientProfile.Role.PATIENT)
def explain_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, patient=request.user)
    generated_explanation = ""
    if request.method == "POST" and request.POST.get("action") == "generate":
        try:
            generated_explanation = explain_medical_record(record)
        except AIServiceUnavailable as exc:
            messages.warning(request, str(exc))
    return render(
        request,
        "care/record_explainer.html",
        {
            "active_nav": "explain",
            "record": record,
            "explanation": generated_explanation or record.plain_language_summary,
        },
    )


@role_required(PatientProfile.Role.CLINICIAN)
def select_records(request, referral_id):
    referral = get_object_or_404(Referral, id=referral_id, clinician=request.user)
    if referral.status != Referral.Status.PENDING:
        messages.info(request, "This referral package is locked after patient review.")
        return redirect("care:doctor_workspace", referral_id=referral.id)
    available_records = referral.patient.medical_records.filter(status=MedicalRecord.Status.AVAILABLE)
    if request.method == "POST":
        selected_ids = request.POST.getlist("records")
        selected = available_records.filter(id__in=selected_ids)
        if not selected.exists():
            messages.error(request, "Select at least one relevant record.")
        else:
            referral.selected_records.set(selected)
            messages.success(request, "Referral package updated.")
            return redirect("care:select_records", referral_id=referral.id)
    return render(
        request,
        "care/select_records.html",
        {
            "active_nav": "referrals",
            "referral": referral,
            "records": available_records,
            "selected_ids": set(referral.selected_records.values_list("id", flat=True)),
        },
    )


@role_required(PatientProfile.Role.PATIENT)
def patient_consent(request, referral_id):
    referral = _patient_referral(request.user, referral_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            if request.POST.get("confirm_share") != "on":
                messages.error(request, "Confirm that you understand what will be shared.")
            elif referral.status != Referral.Status.PENDING:
                messages.info(request, "This referral has already been reviewed.")
            else:
                referral.status = Referral.Status.SHARED
                referral.consented_at = timezone.now()
                referral.save(update_fields=["status", "consented_at"])
                AccessLog.objects.create(
                    referral=referral,
                    actor_name=request.user.get_full_name() or request.user.username,
                    organization="Patient account",
                    action=f"Approved sharing of {referral.selected_records.count()} records",
                    occurred_at=referral.consented_at,
                )
                messages.success(request, "Referral records shared with your consent.")
                return redirect("care:referral_tracking", referral_id=referral.id)
        elif action == "reject":
            referral.status = Referral.Status.REJECTED
            referral.save(update_fields=["status"])
            messages.info(request, "Referral sharing request rejected.")
            return redirect("care:dashboard")
    return render(
        request,
        "care/patient_consent.html",
        {"active_nav": "referrals", "referral": referral},
    )


@role_required(PatientProfile.Role.PATIENT)
def referral_tracking(request, referral_id):
    referral = _patient_referral(request.user, referral_id)
    return render(
        request,
        "care/referral_tracking.html",
        {"active_nav": "referrals", "referral": referral},
    )


@role_required(PatientProfile.Role.CLINICIAN)
def doctor_workspace(request, referral_id):
    referral = get_object_or_404(
        Referral.objects.prefetch_related("selected_records", "access_logs"),
        id=referral_id,
        clinician=request.user,
    )
    if referral.status in {Referral.Status.PENDING, Referral.Status.REJECTED}:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    return render(
        request,
        "care/doctor_workspace.html",
        {"active_nav": "referrals", "referral": referral},
    )


@role_required(PatientProfile.Role.CLINICIAN)
@require_POST
def update_referral_status(request, referral_id):
    referral = get_object_or_404(Referral, id=referral_id, clinician=request.user)
    requested_status = request.POST.get("status")
    transitions = {
        Referral.Status.SHARED: {Referral.Status.RECEIVED},
        Referral.Status.RECEIVED: {Referral.Status.CLOSED},
    }
    if requested_status not in transitions.get(referral.status, set()):
        messages.error(request, "That referral status change is not allowed.")
        return redirect("care:doctor_workspace", referral_id=referral.id)
    referral.status = requested_status
    update_fields = ["status"]
    if requested_status == Referral.Status.RECEIVED:
        referral.received_at = timezone.now()
        update_fields.append("received_at")
    referral.save(update_fields=update_fields)
    AccessLog.objects.create(
        referral=referral,
        actor_name=request.user.get_full_name() or request.user.username,
        organization=getattr(request.user.profile, "organization", ""),
        action=f"Referral marked {referral.get_status_display().lower()}",
        occurred_at=timezone.now(),
    )
    messages.success(request, "Referral status updated.")
    return redirect("care:doctor_workspace", referral_id=referral.id)


@role_required(PatientProfile.Role.PATIENT)
def privacy_access(request):
    referrals = request.user.referrals.prefetch_related("access_logs")
    logs = AccessLog.objects.filter(referral__patient=request.user).select_related("referral")
    return render(
        request,
        "care/privacy_access.html",
        {"active_nav": "privacy", "referrals": referrals, "logs": logs},
    )


@role_required(PatientProfile.Role.PATIENT)
def emergency_profile(request):
    active_medication = request.user.medications.filter(active=True).first()
    return render(
        request,
        "care/emergency_profile.html",
        {
            "active_nav": "profile",
            "active_medication": active_medication,
        },
    )
