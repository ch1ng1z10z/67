# common/validators.py
from datetime import date
from rest_framework.exceptions import ValidationError

def validate_user_age_from_token(request):
    payload = request.auth

    if not payload or not payload.get("birthdate"):
        raise ValidationError(
            "Укажите дату рождения, чтобы создать продукт."
        )

    birthdate = date.fromisoformat(payload["birthdate"])
    today = date.today()

    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

    if age < 18:
        raise ValidationError(
            "Вам должно быть 18 лет, чтобы создать продукт."
        )
