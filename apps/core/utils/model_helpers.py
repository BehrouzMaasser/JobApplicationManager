def normalize_text_fields(instance, fields: list[str], set_to: str | None):

    for field in fields:
        value = getattr(instance, field, None)

        if not value or not value.strip():
            setattr(instance, field, set_to)
