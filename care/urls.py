from django.urls import path

from . import views

app_name = "care"

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.healthcheck, name="healthcheck"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("timeline/", views.timeline, name="timeline"),
    path("records/", views.records, name="records"),
    path("records/add/", views.add_record, name="add_record"),
    path("records/<int:record_id>/download/", views.download_record, name="download_record"),
    path("records/<int:record_id>/explain/", views.explain_record, name="explain_record"),
    path(
        "referrals/<int:referral_id>/select-records/", views.select_records, name="select_records"
    ),
    path("referrals/<int:referral_id>/consent/", views.patient_consent, name="patient_consent"),
    path(
        "referrals/<int:referral_id>/tracking/", views.referral_tracking, name="referral_tracking"
    ),
    path("referrals/<int:referral_id>/workspace/", views.doctor_workspace, name="doctor_workspace"),
    path(
        "referrals/<int:referral_id>/status/",
        views.update_referral_status,
        name="update_referral_status",
    ),
    path("privacy/", views.privacy_access, name="privacy_access"),
    path("profile/emergency/", views.emergency_profile, name="emergency_profile"),
]
