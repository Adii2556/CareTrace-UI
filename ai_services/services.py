import json
import urllib.error
import urllib.request

from django.conf import settings


class AIServiceUnavailable(RuntimeError):
    pass


def explain_medical_record(record) -> str:
    """Return a plain-language explanation without exposing credentials to the browser."""
    if not settings.NVIDIA_API_KEY:
        raise AIServiceUnavailable("AI explanation is temporarily unavailable.")

    prompt = (
        "Explain this fictional medical record in plain language. Do not diagnose, "
        "prescribe treatment, or claim clinical certainty. Encourage the patient to ask a clinician.\n\n"
        f"Title: {record.title}\nCategory: {record.get_category_display()}\n"
        f"Provider: {record.provider}\nSummary: {record.summary}"
    )
    payload = json.dumps(
        {
            "model": settings.NVIDIA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 500,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {settings.NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        raise AIServiceUnavailable("AI explanation is temporarily unavailable.") from exc

    try:
        content = result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise AIServiceUnavailable("AI returned an invalid response.") from exc
    if not content:
        raise AIServiceUnavailable("AI returned an empty response.")
    return content
