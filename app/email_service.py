from sqlalchemy.orm import Session

import requests

from app.config import settings
from app.db_models import NewsletterSubscriber


def _send_template(template_id: int, to: str, params: dict) -> bool:
    if not settings.BREVO_API_KEY:
        print("=" * 60)
        print("BREVO DISABLED (no API key)")
        print(f"  To:   {to}")
        print(f"  Template: {template_id}")
        print(f"  Params: {params}")
        print("=" * 60)
        return True

    payload = {
        "templateId": template_id,
        "to": [{"email": to}],
        "params": params,
    }

    resp = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers={
            "api-key": settings.BREVO_API_KEY,
            "Content-Type": "application/json",
        },
        timeout=15,
    )

    if not resp.ok:
        print(f"BREVO ERROR {resp.status_code}: {resp.text[:300]}")
        return False

    return True


def send_welcome_email(to: str, name: str) -> bool:
    return _send_template(settings.BREVO_WELCOME_TEMPLATE_ID, to, {"name": name})


def send_password_reset_email(to: str, reset_link: str) -> bool:
    return _send_template(
        settings.BREVO_RESET_TEMPLATE_ID,
        to,
        {"name": to, "reset_link": reset_link},
    )


def send_order_confirmation_email(
    to: str, name: str, order_id: int, total: float, items: list[dict]
) -> bool:
    items_text = ", ".join(
        f"{item['plant_name']} x{item['quantity']}" for item in items
    )
    return _send_template(
        settings.BREVO_ORDER_TEMPLATE_ID,
        to,
        {
            "name": name,
            "order_id": order_id,
            "total": f"{total:.2f}",
            "items": items_text,
        },
    )


def subscribe_newsletter(email: str, db: Session) -> bool:
    existing = db.query(NewsletterSubscriber).filter_by(email=email).first()
    if existing:
        return True

    subscriber = NewsletterSubscriber(email=email)
    db.add(subscriber)
    db.flush()

    ok = _send_template(3, email, {"email": email})
    if not ok:
        db.rollback()
        return False

    db.commit()
    return True
