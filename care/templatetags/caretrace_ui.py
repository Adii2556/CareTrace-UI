import json
from functools import lru_cache
from html import escape
from pathlib import Path

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@lru_cache(maxsize=1)
def _icons():
    icon_path = Path(settings.BASE_DIR) / "static" / "icons" / "lucide.json"
    return json.loads(icon_path.read_text(encoding="utf-8"))


@register.simple_tag
def icon(name, class_name=""):
    nodes = _icons().get(str(name), _icons().get("FileText", []))
    parts = [
        f'<svg class="{escape(class_name)}" data-icon="{escape(str(name))}" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    ]
    for tag_name, attributes in nodes:
        attrs = " ".join(f'{escape(key)}="{escape(str(value))}"' for key, value in attributes.items())
        parts.append(f"<{tag_name} {attrs}></{tag_name}>")
    parts.append("</svg>")
    return mark_safe("".join(parts))


@register.filter
def status_class(status):
    return {
        "pending": "amber",
        "approved": "green",
        "shared": "green",
        "received": "",
        "closed": "neutral",
        "rejected": "red",
    }.get(status, "neutral")

