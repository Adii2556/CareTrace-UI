def caretrace_shell(request):
    if not request.user.is_authenticated:
        return {}
    profile = getattr(request.user, "profile", None)
    pending_count = 0
    default_explain_record = None
    if profile and profile.role == "patient":
        pending_count = request.user.referrals.filter(status="pending").count()
        default_explain_record = request.user.medical_records.filter(
            status="available", category="lab"
        ).first()
    return {
        "profile": profile,
        "pending_referral_count": pending_count,
        "default_explain_record": default_explain_record,
    }
